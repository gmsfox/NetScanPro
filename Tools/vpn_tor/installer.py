import subprocess
from colorama import init, Fore, Style
from core.updates import update_dependencies_crossplatform

class VPNTorInstaller:
    def __init__(self):
        """Inicializa com todos os pacotes necessários"""
        self.required_packages = ["tor", "torbrowser-launcher", "obfs4proxy"]
        self.kali_key = "827C8569F2518CC677FECA1AED65462EC8D5E4C5"
        self.tor_key_url = "https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc"

    def check_installation(self):
        """Verifica se todos os pacotes estão instalados corretamente"""
        try:
            for pkg in self.required_packages:
                result = subprocess.run(
                    ["which", pkg],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
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
        """Executa o processo completo de instalação"""
        if self.check_installation():
            print(f"{Fore.BLUE}[!] Pacotes já estão instalados")
            return True

        print(f"{Fore.CYAN}\n[*] Iniciando instalação do Tor...")

        # 1. Corrigir repositórios Kali
        if not self._run_command([
            "sudo", "apt-key", "adv", "--keyserver",
            "keyserver.ubuntu.com", "--recv-keys", self.kali_key
        ]):
            return False

        # 2. Configurar repositório Tor
        repo_cmd = [
            "sudo", "sh", "-c",
            "echo 'deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] "
            "https://deb.torproject.org/torproject.org kali main' > "
            "/etc/apt/sources.list.d/tor.list"
        ]
        if not self._run_command(repo_cmd):
            return False

        # 3. Adicionar chave GPG
        gpg_cmd = (
            f"wget -qO- {self.tor_key_url} | "
            "sudo gpg --dearmor -o /usr/share/keyrings/tor-archive-keyring.gpg"
        )
        if not self._run_command(gpg_cmd, shell=True):
            return False

        # 4. Instalar pacotes
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