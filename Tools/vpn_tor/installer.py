# Tools/vpn_tor/installer.py
import subprocess
from colorama import init, Fore, Style
from core.updates import update_dependencies_crossplatform

class VPNTorInstaller:
    def __init__(self):
        """Inicializa a classe com os pacotes necessários"""
        self.required_packages = ["tor", "torbrowser-launcher", "obfs4proxy"]
        self.key_url = "https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc"
        self.keyring_path = "/usr/share/keyrings/tor-archive-keyring.gpg"

    def _run_command(self, command, shell=False):
        """Método auxiliar para executar comandos"""
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
            print(f"{Fore.RED}Erro ao executar: {' '.join(command) if isinstance(command, list) else command}")
            print(f"{Fore.YELLOW}Detalhes: {e.stderr.strip()}")
            return False

    def check_installation(self):
        """Verifica se todos os pacotes estão instalados"""
        for pkg in self.required_packages:
            if not self._run_command(["which", pkg]):
                return False
        return True

    def install_all(self):
        """Executa o processo completo de instalação"""
        if self.check_installation():
            print(f"{Fore.BLUE}[!] Pacotes já estão instalados")
            return True

        print(f"{Fore.YELLOW}[*] Configurando ambiente Tor...")

        # 1. Configurar repositório
        repo_cmd = [
            "sudo", "sh", "-c",
            f"echo 'deb [signed-by={self.keyring_path}] "
            f"https://deb.torproject.org/torproject.org kali main' > "
            "/etc/apt/sources.list.d/tor.list"
        ]

        # 2. Adicionar chave GPG
        gpg_cmd = (
            f"wget -qO- {self.key_url} | "
            f"sudo gpg --dearmor -o {self.keyring_path}"
        )

        # 3. Instalar pacotes
        install_cmd = ["sudo", "apt", "install", "-y"] + self.required_packages

        # Executar todos os comandos em sequência
        steps = [
            (repo_cmd, False),
            (gpg_cmd, True),
            (["sudo", "apt", "update"], False),
            (install_cmd, False)
        ]

        for cmd, use_shell in steps:
            if not self._run_command(cmd, shell=use_shell):
                return False

        if self.check_installation():
            print(f"{Fore.GREEN}[✔] Instalação concluída com sucesso!")
            return True

        print(f"{Fore.RED}[✘] A instalação não foi concluída corretamente")
        return False