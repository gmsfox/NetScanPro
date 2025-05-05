# Tools/vpn_tor/installer.py
import subprocess
from colorama import init, Fore, Style
from core.updates import update_dependencies_crossplatform

class VPNTorInstaller:
    def __init__(self):
        self.required_packages = ["tor", "torbrowser-launcher", "obfs4proxy"]
        self.installed = False

    def check_installation(self):
        """Verifica se todos os pacotes necessários estão instalados"""
        try:
            for pkg in self.required_packages:
                result = subprocess.run(["which", pkg],
                                      capture_output=True,
                                      text=True)
                if result.returncode != 0:
                    return False
            return True
        except Exception:
            return False

    def install_all(self):
        """Instala todos os componentes necessários de forma robusta"""
        if self.check_installation():
            print(f"{Fore.BLUE}[!] Pacotes já estão instalados")
            return True

        try:
            print(f"{Fore.YELLOW}[*] Configurando repositórios Tor...")

            # 1. Configurar repositório e chave GPG
            subprocess.run([
                "sudo", "sh", "-c",
                "echo 'deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] "
                "https://deb.torproject.org/torproject.org kali main' > "
                "/etc/apt/sources.list.d/tor.list"
            ], check=True)

            subprocess.run([
                "wget", "-qO-",
                "https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc",
                "|", "sudo", "gpg", "--dearmor",
                "-o", "/usr/share/keyrings/tor-archive-keyring.gpg"
            ], shell=True, check=True)

            # 2. Atualizar e instalar
            print(f"{Fore.YELLOW}[*] Instalando pacotes...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run([
                "sudo", "apt", "install", "-y"
            ] + self.required_packages, check=True)

            # 3. Verificar instalação
            if self.check_installation():
                print(f"{Fore.GREEN}[✔] Instalação concluída com sucesso!")
                self.installed = True
                return True

            print(f"{Fore.RED}[✘] Instalação incompleta")
            return False

        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}[✘] Erro durante instalação: {e.stderr or str(e)}")
            return False
        except Exception as e:
            print(f"{Fore.RED}[✘] Erro inesperado: {str(e)}")
            return False