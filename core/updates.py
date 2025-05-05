import subprocess
import os
from colorama import Fore

def update_dependencies_crossplatform():
    """Atualiza dependências de forma multiplataforma."""
    try:
        print(f"{Fore.YELLOW}Atualizando dependências do sistema...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)
        print(f"{Fore.GREEN}Dependências atualizadas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Erro ao atualizar dependências: {e}")