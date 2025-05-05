import subprocess
from colorama import init, Fore, Style
from core.updates import update_dependencies_crossplatform

class VPNTorInstaller:
    def __init__(self):
        """Inicializador da classe com todos os atributos necessários"""
        self.required_packages = ["tor", "torbrowser-launcher", "obfs4proxy"]
        self.tor_key_url = "https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc"
        self.keyring_path = "/usr/share/keyrings/tor-archive-keyring.gpg"

    def check_installation(self):
        """Verifica se todos os pacotes estão instalados"""
        try:
            for pkg in self.required_packages:  # Note o uso de self aqui
                result = subprocess.run(
                    ["dpkg", "-l", pkg],
                    capture_output=True,
                    text=True
                )
                if "ii" not in result.stdout:
                    return False
            return True
        except Exception as e:
            print(f"{Fore.RED}Erro na verificação: {str(e)}")
            return False

    def _run_command(self, command, shell=False):
        """Método auxiliar para executar comandos"""
        try:
            subprocess.run(
                command,
                shell=shell,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Erro no comando: {' '.join(e.cmd) if isinstance(e.cmd, list) else e.cmd}")
            print(f"{Fore.YELLOW}Saída: {e.stderr.decode().strip()}")
            return False

    def install_all(self):
        """Método principal de instalação"""
        if self.check_installation():  # Usando self para acessar o método
            print(f"{Fore.BLUE}[!] Pacotes já estão instalados")
            return True

        print(f"{Fore.CYAN}\n[*] Iniciando instalação do Tor...")

        try:
            # 1. Baixar chave GPG
            if not self._run_command([  # Usando self para acessar o método
                "sudo", "wget", "-qO", "/tmp/tor-key.asc",
                self.tor_key_url  # Usando self para acessar o atributo
            ]):
                return False

            # 2. Instalar chave
            if not self._run_command([
                "sudo", "gpg", "--dearmor",
                "-o", self.keyring_path,  # Usando self para acessar o atributo
                "/tmp/tor-key.asc"
            ]):
                return False

            # 3. Configurar repositório
            repo_line = f"deb [signed-by={self.keyring_path}] https://deb.torproject.org/torproject.org kali main"
            if not self._run_command([
                "sudo", "sh", "-c",
                f"echo '{repo_line}' > /etc/apt/sources.list.d/tor.list"
            ]):
                return False

            # 4. Instalar pacotes
            commands = [
                ["sudo", "apt", "update"],
                ["sudo", "apt", "install", "-y"] + self.required_packages,  # Usando self
                ["sudo", "systemctl", "enable", "--now", "tor"]
            ]

            for cmd in commands:
                if not self._run_command(cmd):
                    return False

            print(f"{Fore.GREEN}[✔] Instalação concluída com sucesso!")
            return True

        except Exception as e:
            print(f"{Fore.RED}[✘] Erro inesperado: {str(e)}")
            return False