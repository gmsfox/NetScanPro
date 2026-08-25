import os
import subprocess
import requests
import time
import hashlib
import shutil
import logging
import re
from typing import Tuple, List, Dict
from pathlib import Path
import platform
from colorama import Fore

class VPNManager:
    # Configurações
    VPN_DIR = Path(__file__).parent / "PROTONVPN"
    OFFICIAL_REPO = {
        "stable": {
            "package": "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.8_all.deb",
            "checksum": "0b14e71586b22e498eb20926c48c7b434b751149b1f2af9902ef1cfe6b03e180"
        },
        "beta": {
            "package": "https://repo.protonvpn.com/debian/dists/unstable/main/binary-all/protonvpn-beta-release_1.0.8_all.deb",
            "checksum": "0f3c88b11aae384d76fc63547c4fbea1161c2aef376fb4b73d32786cbf9fa019"
        }
    }

    @staticmethod
    def _run_command(cmd: List[str], check: bool = True) -> Tuple[bool, str]:
        """Executa um comando e retorna o resultado."""
        try:
            result = subprocess.run(
                cmd,
                check=check,
                capture_output=True,
                text=True
            )
            output = result.stdout.strip() or result.stderr.strip()
            return result.returncode == 0, output
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip() if e.stderr else str(e)
        except FileNotFoundError:
            return False, "Comando não encontrado. Verifique se o programa está instalado."

    @staticmethod
    def _create_vpn_dir() -> Tuple[bool, str]:
        """Cria o diretório PROTONVPN se não existir."""
        try:
            VPNManager.VPN_DIR.mkdir(exist_ok=True, parents=True)
            return True, "Diretório PROTONVPN criado/verificado"
        except Exception as e:
            return False, f"Erro ao criar diretório: {str(e)}"

    @staticmethod
    def _download_file(url: str, dest: Path) -> Tuple[bool, str]:
        """Baixa um arquivo da URL para o destino especificado."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(dest, 'wb') as f:
                f.write(response.content)
            return True, f"Arquivo baixado: {dest}"
        except requests.exceptions.RequestException as e:
            return False, f"Falha no download: {str(e)}"

    @staticmethod
    def _verify_checksum(file_path: Path, expected_checksum: str) -> Tuple[bool, str]:
        """Verifica o checksum SHA256 de um arquivo."""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            file_checksum = sha256_hash.hexdigest()
            if file_checksum == expected_checksum:
                return True, "Checksum verificado com sucesso"
            else:
                return False, f"Checksum inválido. Esperado: {expected_checksum}, Obtido: {file_checksum}"
        except Exception as e:
            return False, f"Erro ao verificar checksum: {str(e)}"

    @staticmethod
    def _install_dependencies() -> Tuple[bool, str]:
        """Instala somente as dependências Linux que ainda não existem."""
        deps = [
            "ca-certificates", "wget", "gnupg"
        ]

        missing_deps = []
        for package in deps:
            success, status = VPNManager._run_command(
                ["dpkg-query", "-W", "-f=${Status}", package], check=False
            )
            if not success or status != "install ok installed":
                missing_deps.append(package)

        if not missing_deps:
            return True, "Dependências já instaladas"

        success, msg = VPNManager._run_command(["sudo", "apt-get", "update"])
        if not success:
            return False, f"Falha ao atualizar índices do APT: {msg}"

        return VPNManager._run_command(
            ["sudo", "apt-get", "install", "-y"] + missing_deps
        )

    @staticmethod
    def _install_protonvpn(repo_type: str = "stable") -> Tuple[bool, str]:
        repo_info = VPNManager.OFFICIAL_REPO[repo_type]
        package_url = repo_info["package"]
        package_name = package_url.split('/')[-1]
        package_path = VPNManager.VPN_DIR / package_name

        success, msg = VPNManager._download_file(package_url, package_path)
        if not success:
            return False, msg

        success, msg = VPNManager._verify_checksum(package_path, repo_info["checksum"])
        if not success:
            return False, msg

        # Instala o pacote local que configura o repositório oficial.
        try:
            result = subprocess.run(
                ["sudo", "dpkg", "-i", str(package_path)],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                repair = subprocess.run(
                    ["sudo", "apt-get", "install", "-f", "-y"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if repair.returncode != 0:
                    return False, repair.stderr.strip() or result.stderr.strip()
        except OSError as e:
            return False, f"Erro ao instalar o pacote do repositório: {e}"

        success, msg = VPNManager._run_command(["sudo", "apt-get", "update"])
        if not success:
            return False, msg

        for package in ["protonvpn-cli", "protonvpn-cli-ng"]:
            success, msg = VPNManager._run_command(
                ["sudo", "apt-get", "install", "-y", package]
            )
            if success:
                return True, f"ProtonVPN ({repo_type}) instalado com sucesso"

        return False, msg or "Não foi possível instalar um CLI compatível do ProtonVPN"

    @staticmethod
    def check_installation() -> Tuple[bool, str]:
        """Verifica se o ProtonVPN CLI está instalado corretamente."""
        for cmd in ["protonvpn-cli-ng", "protonvpn-cli", "protonvpn"]:
            if shutil.which(cmd):
                return True, "ProtonVPN está instalado"
        return False, "ProtonVPN não encontrado"

    @staticmethod
    def get_connection_status() -> Tuple[bool, str]:
        """Verifica se está conectado à VPN."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "VPN não instalada"

        cli_cmd = VPNManager._get_cli_command()
        if not cli_cmd:
            return False, "Comando VPN não encontrado"

        try:
            success, output = VPNManager._run_command([cli_cmd, "status"], check=False)
            output_lower = output.lower()
            if re.search(r"\b(disconnected|off|not connected)\b", output_lower):
                return False, "VPN desconectada"
            if success and re.search(r"\b(connected|on)\b", output_lower):
                return True, "VPN conectada"
        except Exception:
            pass

        return False, "Status desconhecido"

    @staticmethod
    def quick_connect() -> Tuple[bool, str]:
        """Conecta rápido à VPN (servidor mais rápido)."""
        installed, msg = VPNManager.check_installation()
        if not installed:
            return False, msg

        cli_cmd = VPNManager._get_cli_command()
        if not cli_cmd:
            return False, "Comando VPN não encontrado"

        return VPNManager._run_command(["sudo", cli_cmd, "connect", "--fastest"], check=False)

    @staticmethod
    def quick_disconnect() -> Tuple[bool, str]:
        """Desconecta rápido da VPN."""
        installed, msg = VPNManager.check_installation()
        if not installed:
            return False, msg

        cli_cmd = VPNManager._get_cli_command()
        if not cli_cmd:
            return False, "Comando VPN não encontrado"

        return VPNManager._run_command(["sudo", cli_cmd, "disconnect"], check=False)

    @staticmethod
    def install() -> Tuple[bool, str]:
        """Fluxo completo de instalação com verificação de sistema."""
        if platform.system() != "Linux":
            return False, "Instalação só é suportada em Linux"

        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "debian" not in content and "ubuntu" not in content:
                    return False, "Sistema não baseado em Debian/Ubuntu"
        except:
            return False, "Não foi possível verificar a distribuição"

        success, msg = VPNManager._create_vpn_dir()
        if not success:
            return False, msg

        print(f"{Fore.CYAN}▶ Instalando dependências...")
        success, msg = VPNManager._install_dependencies()
        if not success:
            return False, msg

        print(f"{Fore.CYAN}▶ Instalando versão estável...")
        success, msg = VPNManager._install_protonvpn("stable")
        if not success:
            print(f"{Fore.YELLOW}▶ Tentando versão beta...")
            success, msg = VPNManager._install_protonvpn("beta")
            if not success:
                return False, msg

        return True, "ProtonVPN instalado com sucesso"

    @staticmethod
    def quick_install() -> Tuple[bool, str]:
        """One-click installation - automatically installs with minimal prompts."""
        print(f"{Fore.CYAN}╔═══════════════════════════════════════╗")
        print(f"{Fore.CYAN}║  INSTALAÇÃO ONE-CLICK DO PROTONVPN    ║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
        print()
        print(f"{Fore.YELLOW}Este processo irá:")
        print(f"{Fore.YELLOW}  • Atualizar repositórios")
        print(f"{Fore.YELLOW}  • Instalar dependências")
        print(f"{Fore.YELLOW}  • Baixar e instalar ProtonVPN CLI")
        print()

        confirm = input(f"{Fore.CYAN}Deseja continuar? (s/n): ").lower()
        if confirm != "s":
            return False, "Instalação cancelada pelo usuário"

        print()
        return VPNManager.install()

    @staticmethod
    def uninstall() -> Tuple[bool, str]:
        """Desinstala completamente o ProtonVPN."""
        try:
            commands = [
                ["sudo", "apt", "remove", "--purge", "-y", "protonvpn*"],
                ["sudo", "apt", "autoremove", "-y"],
                ["sudo", "rm", "-rf", "/etc/apt/sources.list.d/protonvpn*"],
                ["sudo", "rm", "-rf", "/usr/share/keyrings/protonvpn*"],
                ["sudo", "apt", "update"]
            ]
            for cmd in commands:
                success, msg = VPNManager._run_command(cmd, check=False)
                if not success:
                    logging.warning(f"Falha ao executar {cmd}: {msg}")

            home_dir = Path.home()
            protonvpn_dirs = [
                home_dir / ".cache/protonvpn",
                home_dir / ".config/protonvpn",
                home_dir / ".local/share/protonvpn"
            ]
            for dir_path in protonvpn_dirs:
                if dir_path.exists():
                    shutil.rmtree(dir_path, ignore_errors=True)

            return True, "ProtonVPN foi desinstalado com sucesso"
        except Exception as e:
            return False, f"Erro durante a desinstalação: {str(e)}"

    @staticmethod
    def _get_cli_command() -> str:
        """Retorna o comando CLI disponível para o ProtonVPN."""
        for cmd in ["protonvpn-cli", "protonvpn-cli-ng", "protonvpn"]:
            if shutil.which(cmd):
                return cmd
        return ""

    @staticmethod
    def connect() -> Tuple[bool, str]:
        """Conecta à VPN usando o servidor mais rápido."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"
        cli_cmd = VPNManager._get_cli_command()
        if not cli_cmd:
            return False, "Nenhum comando ProtonVPN CLI encontrado"
        return VPNManager._run_command(["sudo", cli_cmd, "connect", "--fastest"])

    @staticmethod
    def disconnect() -> Tuple[bool, str]:
        """Desconecta da VPN."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"
        cli_cmd = VPNManager._get_cli_command()
        if not cli_cmd:
            return False, "Nenhum comando ProtonVPN CLI encontrado"
        return VPNManager._run_command(["sudo", cli_cmd, "disconnect"])

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verifica o status da conexão VPN."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"
        cli_cmd = VPNManager._get_cli_command()
        if not cli_cmd:
            return False, "Nenhum comando ProtonVPN CLI encontrado"
        return VPNManager._run_command([cli_cmd, "status"], check=False)

    @staticmethod
    def check_updates() -> Tuple[bool, str]:
        """Verifica se há atualizações disponíveis."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"

        commands = [
            ["sudo", "apt", "update"],
            ["apt", "list", "--upgradable"]
        ]
        for cmd in commands:
            success, msg = VPNManager._run_command(cmd)
            if not success:
                return False, msg

        success, msg = VPNManager._run_command(["apt", "list", "--upgradable", "protonvpn*"])
        if "protonvpn" in msg.lower():
            return True, "Atualizações disponíveis para o ProtonVPN"
        return True, "O ProtonVPN está atualizado"

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Configura o login do ProtonVPN."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"
        cli_cmd = VPNManager._get_cli_command()
        if not cli_cmd:
            return False, "Nenhum comando ProtonVPN CLI encontrado"
        return VPNManager._run_command(["sudo", cli_cmd, "login", username, password])

    @staticmethod
    def setup_repository() -> Tuple[bool, str]:
        """Configura o repositório oficial do ProtonVPN."""
        try:
            # Adiciona a chave do repositório
            subprocess.run(
                'wget -q -O- https://repo.protonvpn.com/debian/public_key.asc | sudo tee /etc/apt/trusted.gpg.d/protonvpn.asc',
                shell=True,
                check=True
            )
            # Adiciona o repositório à lista de fontes
            VPNManager._run_command(["sudo", "add-apt-repository", "deb https://repo.protonvpn.com/debian stable main"])
            # Atualiza a lista de pacotes
            VPNManager._run_command(["sudo", "apt", "update"])
            return True, "Repositório do ProtonVPN configurado com sucesso"
        except Exception as e:
            return False, f"Erro ao configurar repositório: {str(e)}"
