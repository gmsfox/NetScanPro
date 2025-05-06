import subprocess
import logging
from colorama import Fore
import os

class VPNManager:
    @staticmethod
    def check_installation() -> bool:
        """Verifica se o protonvpn-cli está instalado."""
        try:
            subprocess.run(["protonvpn-cli", "--version"],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    @staticmethod
    def check_connection() -> bool:
        """Verifica se a VPN está ativa."""
        try:
            result = subprocess.run(["protonvpn-cli", "status"],
                                   capture_output=True,
                                   text=True,
                                   check=True)
            return "Connected" in result.stdout
        except subprocess.SubprocessError as e:
            logging.error(f"Erro ao verificar status da VPN: {str(e)}")
            return False

    @staticmethod
    def connect() -> str:
        """Conecta à ProtonVPN."""
        try:
            subprocess.run(["protonvpn-cli", "connect", "--fastest"],
                          check=True)
            return "success"
        except subprocess.SubprocessError as e:
            logging.error(f"Falha na conexão VPN: {str(e)}")
            return str(e)

    @staticmethod
    def disconnect() -> str:
        """Desconecta da ProtonVPN."""
        try:
            subprocess.run(["protonvpn-cli", "disconnect"],
                          check=True)
            return "success"
        except subprocess.SubprocessError as e:
            logging.error(f"Falha ao desconectar VPN: {str(e)}")
            return str(e)

    @staticmethod
    def install() -> str:
        """Instala/Atualiza a ProtonVPN."""
        install_commands = [
            ["sudo", "apt", "update"],
            ["wget", "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.3_all.deb"],
            ["sudo", "dpkg", "-i", "protonvpn-stable-release_1.0.3_all.deb"],
            ["sudo", "apt", "update"],
            ["sudo", "apt", "install", "-y", "protonvpn"]
        ]

        try:
            for cmd in install_commands:
                subprocess.run(cmd, check=True)
            os.remove("protonvpn-stable-release_1.0.3_all.deb")
            return "success"
        except subprocess.SubprocessError as e:
            logging.error(f"Erro na instalação: {str(e)}")
            return str(e)