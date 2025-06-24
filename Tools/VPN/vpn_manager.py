import os
import subprocess
import requests
import time
from typing import Tuple, List, Dict
from pathlib import Path

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
            return True, result.stdout.strip()
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
            import hashlib
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
        """Instala dependências necessárias."""
        deps = [
            "wget", "apt-transport-https", "gnupg",
            "libayatana-appindicator3-1",
            "gir1.2-ayatanaappindicator3-0.1",
            "gnome-shell-extension-appindicator"
        ]
        return VPNManager._run_command(
            ["sudo", "apt", "install", "-y"] + deps
        )

    @staticmethod
    def _install_protonvpn(repo_type: str = "stable") -> Tuple[bool, str]:
        """Instala o ProtonVPN a partir do repositório especificado."""
        # 1. Baixar o pacote do repositório
        repo_info = VPNManager.OFFICIAL_REPO[repo_type]
        package_url = repo_info["package"]
        package_name = package_url.split('/')[-1]
        package_path = VPNManager.VPN_DIR / package_name

        success, msg = VPNManager._download_file(package_url, package_path)
        if not success:
            return False, msg

        # 2. Verificar checksum
        success, msg = VPNManager._verify_checksum(package_path, repo_info["checksum"])
        if not success:
            return False, msg

        # 3. Instalar o pacote do repositório
        commands = [
            ["sudo", "dpkg", "-i", str(package_path)],
            ["sudo", "apt", "update"],
            ["sudo", "apt", "install", "-y", "protonvpn-gnome-desktop", "protonvpn-cli"],
            ["sudo", "apt", "--fix-broken", "install", "-y"]
        ]

        for cmd in commands:
            success, msg = VPNManager._run_command(cmd)
            if not success:
                return False, msg

        return True, f"ProtonVPN ({repo_type}) instalado com sucesso"

    @staticmethod
    def check_installation() -> Tuple[bool, str]:
        """Verifica se o ProtonVPN está instalado."""
        # Verifica tanto o CLI quanto o GUI
        cli_installed = VPNManager._run_command(["which", "protonvpn-cli"], check=False)[0]
        gui_installed = VPNManager._run_command(["which", "protonvpn"], check=False)[0]

        if cli_installed or gui_installed:
            return True, "ProtonVPN está instalado"
        return False, "ProtonVPN não encontrado"

    @staticmethod
    def install() -> Tuple[bool, str]:
        """Fluxo completo de instalação do ProtonVPN."""
        # 1. Criar diretório se não existir
        success, msg = VPNManager._create_vpn_dir()
        if not success:
            return False, msg

        # 2. Instalar dependências
        success, msg = VPNManager._install_dependencies()
        if not success:
            return False, msg

        # 3. Tentar instalação estável primeiro
        success, msg = VPNManager._install_protonvpn("stable")
        if not success:
            # Se falhar, tentar versão beta
            success, msg = VPNManager._install_protonvpn("beta")
            if not success:
                return False, msg

        return True, "ProtonVPN instalado com sucesso"

    @staticmethod
    def uninstall() -> Tuple[bool, str]:
        """Desinstala completamente o ProtonVPN e remove todos os registros."""
        # 1. Desinstalar pacotes
        commands = [
            ["sudo", "apt", "autoremove", "-y", "proton-vpn-gnome-desktop", "protonvpn-cli"],
            ["sudo", "apt", "purge", "-y", "protonvpn-stable-release", "protonvpn-beta-release"],
            ["sudo", "rm", "-rf", "/etc/apt/sources.list.d/protonvpn*"],
            ["sudo", "rm", "-rf", "/usr/share/keyrings/protonvpn*"],
            ["sudo", "apt", "update"]
        ]

        for cmd in commands:
            VPNManager._run_command(cmd, check=False)

        # 2. Remover conexões do NetworkManager
        success, connections = VPNManager._run_command(
            ["nmcli", "connection", "show", "--active"]
        )
        if success:
            for line in connections.split('\n'):
                if line.startswith("pvpn-"):
                    conn_name = line.split()[0]
                    VPNManager._run_command(
                        ["nmcli", "connection", "delete", conn_name],
                        check=False
                    )

        # 3. Remover diretório de configuração do usuário
        home_dir = Path.home()
        protonvpn_config = home_dir / ".config/protonvpn"
        if protonvpn_config.exists():
            try:
                import shutil
                shutil.rmtree(protonvpn_config)
            except Exception:
                pass

        return True, "ProtonVPN desinstalado completamente"

    @staticmethod
    def connect() -> Tuple[bool, str]:
        """Conecta à VPN usando o servidor mais rápido."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"
        return VPNManager._run_command(
            ["sudo", "protonvpn-cli", "connect", "--fastest"]
        )

    @staticmethod
    def disconnect() -> Tuple[bool, str]:
        """Desconecta da VPN."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"
        return VPNManager._run_command(
            ["sudo", "protonvpn-cli", "disconnect"]
        )

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verifica o status da conexão VPN."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"
        return VPNManager._run_command(["protonvpn-cli", "status"], check=False)

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

        # Verifica especificamente por atualizações do ProtonVPN
        success, msg = VPNManager._run_command(
            ["apt", "list", "--upgradable", "protonvpn*"]
        )

        if "protonvpn" in msg.lower():
            return True, "Atualizações disponíveis para o ProtonVPN"
        return True, "O ProtonVPN está atualizado"

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Configura o login do ProtonVPN."""
        installed, _ = VPNManager.check_installation()
        if not installed:
            return False, "ProtonVPN não está instalado"

        return VPNManager._run_command(
            ["sudo", "protonvpn-cli", "login", username, password]
        )