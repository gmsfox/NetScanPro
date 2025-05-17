import os
import subprocess
import re
from typing import Tuple

class VPNManager:
    @staticmethod
    def check_installation() -> bool:
        """Verifica se o ProtonVPN está instalado"""
        try:
            result = subprocess.run(["which", "protonvpn"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def _run_command(cmd: list) -> Tuple[bool, str]:
        """Executa comandos com tratamento de erros"""
        try:
            result = subprocess.run(cmd, check=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=300)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip()
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _clean_old_files():
        """Remove todos os arquivos .deb antigos e configurações residuais"""
        try:
            # Limpar pacotes .deb antigos
            for f in os.listdir('.'):
                if f.startswith('protonvpn') and (f.endswith('.deb') or f.endswith('.asc')):
                    os.remove(f)

            # Limpar arquivos de configuração residuais
            residual_files = [
                '/usr/share/keyrings/protonvpn-archive-keyring.gpg',
                '/etc/apt/sources.list.d/protonvpn-stable.list'
            ]

            for file_path in residual_files:
                if os.path.exists(file_path):
                    subprocess.run(["sudo", "rm", "-f", file_path])

        except Exception as e:
            print(f"Warning: Error during cleanup - {str(e)}")

    @staticmethod
    def _install_dependencies() -> Tuple[bool, str]:
        """Instala dependências necessárias"""
        dependencies = ["gnupg", "wget", "gpg", "apt-transport-https", "ca-certificates"]

        # Atualizar primeiro
        success, msg = VPNManager._run_command(["sudo", "apt", "update"])
        if not success:
            return False, f"Failed to update packages: {msg}"

        # Instalar dependências
        success, msg = VPNManager._run_command(
            ["sudo", "apt", "install", "-y"] + dependencies
        )
        if not success:
            return False, f"Failed to install dependencies: {msg}"

        return True, "Dependencies installed successfully"

    @staticmethod
    def _add_gpg_key() -> Tuple[bool, str]:
        """Adiciona a chave GPG do ProtonVPN"""
        try:
            # Método 1: Usando curl (preferencial)
            curl_cmd = [
                "curl", "-fsSL", "https://repo.protonvpn.com/debian/public_key.asc",
                "|", "sudo", "gpg", "--dearmor",
                "--output", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"
            ]

            success, msg = VPNManager._run_command(" ".join(curl_cmd), shell=True)
            if success:
                return True, "GPG key added successfully"

            # Método 2: Alternativo se curl falhar
            wget_cmd = [
                "wget", "-qO-", "https://repo.protonvpn.com/debian/public_key.asc",
                "|", "gpg", "--dearmor",
                "|", "sudo", "tee", "/usr/share/keyrings/protonvpn-archive-keyring.gpg", ">/dev/null"
            ]

            success, msg = VPNManager._run_command(" ".join(wget_cmd), shell=True)
            if not success:
                return False, f"Failed to add GPG key: {msg}"

            return True, "GPG key added successfully"

        except Exception as e:
            return False, f"GPG key error: {str(e)}"

    @staticmethod
    def _setup_repository() -> Tuple[bool, str]:
        """Configura o repositório do ProtonVPN"""
        repo_cmd = (
            'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/protonvpn-archive-keyring.gpg] '
            'https://repo.protonvpn.com/debian stable main" | '
            'sudo tee /etc/apt/sources.list.d/protonvpn-stable.list'
        )

        success, msg = VPNManager._run_command(repo_cmd, shell=True)
        if not success:
            return False, f"Failed to setup repository: {msg}"

        return True, "Repository setup successfully"

    @staticmethod
    def install_protonvpn() -> Tuple[bool, str]:
        """Fluxo completo de instalação do ProtonVPN"""
        try:
            print("\nStarting ProtonVPN installation process...")

            # 1. Limpeza inicial
            print("Cleaning up old files...")
            VPNManager._clean_old_files()

            # 2. Instalar dependências
            print("Installing required dependencies...")
            success, msg = VPNManager._install_dependencies()
            if not success:
                return False, msg

            # 3. Adicionar chave GPG
            print("Adding ProtonVPN GPG key...")
            success, msg = VPNManager._add_gpg_key()
            if not success:
                return False, msg

            # 4. Configurar repositório
            print("Setting up ProtonVPN repository...")
            success, msg = VPNManager._setup_repository()
            if not success:
                return False, msg

            # 5. Atualizar e instalar
            print("Updating package list...")
            success, msg = VPNManager._run_command(["sudo", "apt", "update"])
            if not success:
                return False, f"Failed to update package list: {msg}"

            print("Installing ProtonVPN...")
            success, msg = VPNManager._run_command(["sudo", "apt", "install", "-y", "protonvpn"])
            if not success:
                return False, f"Failed to install ProtonVPN: {msg}"

            return True, "ProtonVPN installed successfully!"

        except Exception as e:
            return False, f"Installation failed: {str(e)}"