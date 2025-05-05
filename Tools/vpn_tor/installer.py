# Tools/vpn_tor/installer.py
import subprocess
from ..core.updates import update_dependencies_crossplatform

class VPNTorInstaller:
    def install_protonvpn(self):
        """Instala ProtonVPN CLI."""
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "openvpn", "python3-pip"], check=True)
            subprocess.run(["sudo", "pip3", "install", "protonvpn-cli"], check=True)
            print("✅ ProtonVPN instalado!")
        except subprocess.CalledProcessError:
            raise Exception("Erro: Dependências desatualizadas. Execute a atualização global.")

    def install_tor(self):
        """Instala e inicia o serviço TOR."""
        subprocess.run(["sudo", "apt", "install", "-y", "tor"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "tor"], check=True)
        print("✅ TOR instalado e ativo!")

    def install_all(self):
        """Instala tudo e verifica dependências."""
        try:
            self.install_tor()
            self.install_protonvpn()
        except subprocess.CalledProcessError:
            update_dependencies_crossplatform()  # Chama a atualização global
            self.install_all()  # Tenta novamente após atualizar