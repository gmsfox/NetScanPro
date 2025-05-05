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
        """Instala TOR e dependências de forma robusta no Kali Linux"""
    try:
        print(f"{Fore.YELLOW}[*] Configurando repositórios...")

        # 1. Adicionar chave GPG do repositório Kali
        subprocess.run([
            "sudo", "apt-key", "adv", "--keyserver", "keyserver.ubuntu.com",
            "--recv-keys", "827C8569F2518CC677FECA1AED65462EC8D5E4C5"
        ], check=True)

        # 2. Adicionar repositório oficial do Tor
        tor_repo = """deb [arch=amd64 signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] \
https://deb.torproject.org/torproject.org kali main"""

        with open("/etc/apt/sources.list.d/tor.list", "w") as f:
            f.write(tor_repo + "\n")

        # 3. Adicionar chave GPG do Tor
        subprocess.run([
            "wget", "-qO-",
            "https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc",
            "|", "sudo", "gpg", "--dearmor", "-o",
            "/usr/share/keyrings/tor-archive-keyring.gpg"
        ], shell=True, check=True)

        # 4. Atualizar e instalar
        print(f"{Fore.YELLOW}[*] Instalando pacotes...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run([
            "sudo", "apt", "install", "-y",
            "tor", "torbrowser-launcher", "obfs4proxy"
        ], check=True)

        print(f"{Fore.GREEN}[✔] Tor instalado com sucesso!")

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode().strip() if e.stderr else str(e)
        print(f"{Fore.RED}[✘] Falha na instalação: {error_msg}")
        print(f"{Fore.YELLOW}Dica: Execute manualmente 'sudo apt update' e verifique sua conexão com a internet")
    except Exception as e:
        print(f"{Fore.RED}[✘] Erro inesperado: {str(e)}")