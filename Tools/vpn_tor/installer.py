import subprocess
from colorama import init, Fore, Style
from core.updates import update_dependencies_crossplatform

class VPNTorInstaller:
    def __init__(self):
        """Inicializa com todos os pacotes necessários"""
        self.required_packages = ["tor", "torbrowser-launcher", "obfs4proxy"]
        self.tor_key_url = "https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc"
        self.keyring_path = "/usr/share/keyrings/tor-archive-keyring.gpg"

    def check_installation(self):
        """Verifica se todos os pacotes estão instalados"""
        try:
            for pkg in self.required_packages:
                result = subprocess.run(
                    ["dpkg", "-l", pkg],
                    capture_output=True,
                    text=True
                )
                if "ii" not in result.stdout:  # ii significa instalado corretamente
                    return False
            return True
        except Exception as e:
            print(f"{Fore.RED}Erro na verificação: {str(e)}")
            return False

    def _run_command(self, command, shell=False):
        """Executa comandos com tratamento de erros"""
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
        """Processo de instalação atualizado para sistemas modernos"""
        if self.check_installation():
            print(f"{Fore.BLUE}[!] Pacotes já estão instalados")
            return True

        print(f"{Fore.CYAN}\n[*] Iniciando instalação do Tor (método moderno)...")

        # 1. Baixar e instalar chave GPG corretamente
        if not self._run_command([
            "sudo", "wget", "-qO-", self.tor_key_url,
            "|", "sudo", "gpg", "--dearmor",
            "-o", self.keyring_path
        ], shell=True):
            return False

        # 2. Configurar repositório Tor
        repo_line = f"deb [signed-by={self.keyring_path}] https://deb.torproject.org/torproject.org kali main"
        if not self._run_command([
            "sudo", "sh", "-c",
            f"echo '{repo_line}' > /etc/apt/sources.list.d/tor.list"
        ]):
            return False

        # 3. Instalar pacotes
        commands = [
            ["sudo", "apt", "update"],
            ["sudo", "apt", "install", "-y"] + self.required_packages,
            ["sudo", "systemctl", "enable", "--now", "tor"]
        ]

        for cmd in commands:
            if not self._run_command(cmd):
                return False

        print(f"{Fore.GREEN}[✔] Instalação concluída com sucesso!")
        return True