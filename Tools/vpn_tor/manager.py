# Tools/vpn_tor/manager.py
import subprocess
from colorama import Fore

class VPNTorManager:
    def __init__(self):
        self.is_connected = False

    def connect(self, use_tor=True):
        """Conecta ao ProtonVPN com ou sem TOR."""
        try:
            cmd = ["protonvpn-cli", "connect"]
            if use_tor:
                cmd.append("--tor")
            subprocess.run(cmd, check=True)
            self.is_connected = True
            print(f"{Fore.GREEN}✅ VPN{' + TOR' if use_tor else ''} ativada!")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}❌ Falha na conexão. Verifique se ProtonVPN está instalado.")

    def disconnect(self):
        """Desconecta a VPN."""
        subprocess.run(["protonvpn-cli", "disconnect"], check=True)
        self.is_connected = False
        print(f"{Fore.YELLOW}⚠️ VPN desconectada.")

    def status(self) -> str:
        """Retorna o status atual."""
        return "connected" if self.is_connected else "disconnected"