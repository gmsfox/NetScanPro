# Tools/vpn_tor/installer.py
import subprocess
from colorama import init, Fore, Style
from core.updates import update_dependencies_crossplatform

class VPNTorInstaller:
    def __init__(self):
        self.required_packages = ["tor", "torbrowser-launcher", "obfs4proxy"]
        self.kali_key = "827C8569F2518CC677FECA1AED65462EC8D5E4C5"
        self.tor_key_url = "https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc"

    def _run_command(self, command, shell=False):
        """Executa comandos com tratamento de erros robusto"""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Erro no comando: {' '.join(e.cmd) if isinstance(e.cmd, list) else e.cmd}")
            print(f"{Fore.YELLOW}Saída: {e.stderr.strip() or e.stdout.strip()}")
            return False

    def _fix_kali_repo(self):
        """Corrige problemas com os repositórios do Kali"""
        print(f"{Fore.YELLOW}[*] Corrigindo repositórios Kali...")
        commands = [
            ["sudo", "apt-key", "adv", "--keyserver", "keyserver.ubuntu.com", "--recv-keys", self.kali_key],
            ["sudo", "apt", "clean"],
            ["sudo", "rm", "-rf", "/var/lib/apt/lists/*"],
            ["sudo", "apt", "update"]
        ]
        for cmd in commands:
            if not self._run_command(cmd):
                return False
        return True

    def install_all(self):
        """Fluxo completo de instalação com tratamento de erros"""
        print(f"{Fore.CYAN}\n[*] Iniciando instalação do Tor...")

        # 1. Corrigir repositórios Kali primeiro
        if not self._fix_kali_repo():
            print(f"{Fore.RED}[✘] Falha ao corrigir repositórios Kali")
            return False

        # 2. Configurar repositório Tor
        print(f"{Fore.YELLOW}[*] Configurando repositório Tor...")
        tor_repo = f"deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org kali main"
        if not self._run_command([
            "sudo", "sh", "-c",
            f"echo '{tor_repo}' > /etc/apt/sources.list.d/tor.list"
        ]):
            return False

        # 3. Adicionar chave GPG do Tor
        print(f"{Fore.YELLOW}[*] Adicionando chave GPG...")
        if not self._run_command(
            f"wget -qO- {self.tor_key_url} | sudo gpg --dearmor -o /usr/share/keyrings/tor-archive-keyring.gpg",
            shell=True
        ):
            return False

        # 4. Instalar pacotes
        print(f"{Fore.YELLOW}[*] Instalando pacotes...")
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