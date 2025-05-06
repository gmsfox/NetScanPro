import subprocess
import logging
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
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logging.error("Failed to check ProtonVPN installation: %s", str(e))
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
            logging.error("Error checking VPN status: %s", str(e))
            return False

    @staticmethod
    def connect() -> str:
        """Conecta à ProtonVPN."""
        try:
            subprocess.run(["protonvpn-cli", "connect", "--fastest"],
                          check=True)
            return "success"
        except subprocess.SubprocessError as e:
            logging.error("VPN connection failed: %s", str(e))
            return str(e)

    @staticmethod
    def disconnect() -> str:
        """Desconecta da ProtonVPN."""
        try:
            subprocess.run(["protonvpn-cli", "disconnect"],
                          check=True)
            return "success"
        except subprocess.SubprocessError as e:
            logging.error("Failed to disconnect VPN: %s", str(e))
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
            logging.error("ProtonVPN installation error: %s", str(e))
            return str(e)
        except OSError as e:
            logging.error("File operation failed during installation: %s", str(e))
            return str(e)
