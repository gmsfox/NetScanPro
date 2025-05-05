# Tools/vpn_tor/installer.py
import subprocess
from colorama import init, Fore, Style
from core.updates import update_dependencies_crossplatform

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
        """Instala TOR e dependências de forma robusta"""
    success = True  # Variável para controlar o estado da instalação

    try:
        print(f"{Fore.YELLOW}[*] Atualizando repositórios...")

        # 1. Adiciona repositório oficial do Tor
        tor_repo = "deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org kali main"
        with open("/etc/apt/sources.list.d/tor.list", "w") as f:
            f.write(tor_repo + "\n")

        # 2. Adiciona chave GPG de forma segura
        keyring_path = "/usr/share/keyrings/tor-archive-keyring.gpg"
        subprocess.run([
            "sudo", "wget", "-qO-",
            "https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc",
            "|", "sudo", "gpg", "--dearmor", "-o", keyring_path
        ], shell=True, check=True)

        # 3. Atualiza e instala pacotes
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run([
            "sudo", "apt", "install", "-y",
            "tor", "torbrowser-launcher", "obfs4proxy"
        ], check=True)

        print(f"{Fore.GREEN}[✔] Tor e dependências instalados com sucesso!")

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[✘] Erro na instalação: {e.stderr.decode().strip() if e.stderr else str(e)}")
        success = False
    except Exception as e:
        print(f"{Fore.RED}[✘] Erro inesperado: {str(e)}")
        success = False