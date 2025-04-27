"""NetScan Pro - Ferramenta de análise de rede.
Ferramenta de rede com funcionalidades de escaneamento e atualização de dependências.
"""

import os
import platform
import subprocess
import sys
import logging
import ctypes
import time
from colorama import init, Fore, Style

# Constantes
LANGUAGE_EN = '1'
LANGUAGE_PT = '2'

# Diretório de logs
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "error.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Configura o logger
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(message: str) -> None:
    """Registra uma mensagem de erro no arquivo de log."""
    logging.error(message)

def clear_console() -> None:
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_admin_privileges() -> None:
    """Garante que o script está sendo executado como administrador."""
    try:
        if platform.system() == "Windows":
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print(Fore.YELLOW + "Reiniciando como administrador...")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)
        else:
            if hasattr(os, "geteuid") and os.geteuid() != 0:
                print(Fore.YELLOW + "Reiniciando como sudo...")
                subprocess.run(["sudo", sys.executable] + sys.argv, check=True)
                sys.exit(0)
    except Exception as e:
        log_error(f"Erro ao tentar elevar privilégios: {e}")
        print(Fore.RED + f"Erro: {e}")
        sys.exit(1)

def ensure_venv_support() -> None:
    """Garante que venv esteja disponível."""
    try:
        import venv
    except ImportError:
        print(Fore.RED + "Seu sistema não suporta ambientes virtuais (venv).")
        print(Fore.YELLOW + "Instale usando: sudo apt install python3-venv")
        input(Fore.YELLOW + "Pressione Enter para sair...")
        sys.exit(1)

def auto_clear(func):
    """Decorator para limpar a tela antes de rodar uma função."""
    def wrapper(*args, **kwargs):
        clear_console()
        result = func(*args, **kwargs)
        time.sleep(1.5)
        return result
    return wrapper

@auto_clear
def welcome_message(user_language: str) -> None:
    """Mensagem de boas-vindas."""
    msg = "Welcome to the NetScan Pro!" if user_language == LANGUAGE_EN else "Bem-vindo ao NetScan Pro!"
    print(Fore.GREEN + Style.BRIGHT + msg.center(50))

@auto_clear
def goodbye_message(user_language: str) -> None:
    """Mensagem de despedida."""
    msg = "Thank you for using NetScan Pro!" if user_language == LANGUAGE_EN else "Obrigado por usar o NetScan Pro!"
    print(Fore.GREEN + Style.BRIGHT + msg.center(50))

@auto_clear
def handle_invalid_option(user_language: str) -> None:
    """Mensagem de opção inválida."""
    msg = "Invalid option. Try again." if user_language == LANGUAGE_EN else "Opção inválida. Tente novamente."
    print(Fore.RED + msg)

def view_logs() -> None:
    """Exibe o conteúdo dos logs."""
    clear_console()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print(Fore.YELLOW + "Nenhum log encontrado.")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def update_tool_from_github() -> None:
    """Atualiza o código a partir do GitHub."""
    clear_console()
    print(Fore.YELLOW + "Atualizando o NetScan Pro...")
    try:
        subprocess.run(["git", "pull", "https://github.com/WeverttonBruno/NetScanPro.git"], check=True)
        print(Fore.GREEN + "[✔] Atualização realizada com sucesso!")
    except subprocess.SubprocessError as e:
        log_error(f"Erro ao atualizar ferramenta: {e}")
        print(Fore.RED + f"Erro: {e}")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def update_dependencies_crossplatform() -> None:
    """Atualiza as dependências usando pipreqs e limpa o requirements.txt."""
    clear_console()
    print(Fore.YELLOW + "Atualizando dependências...")

    ensure_venv_support()

    venv_path = ".venv"
    if not os.path.exists(venv_path):
        print(Fore.CYAN + "Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

    python_bin = os.path.join(
        venv_path, "Scripts", "python.exe"
    ) if platform.system() == "Windows" else os.path.join(venv_path, "bin", "python3")

    try:
        # Instalar pipreqs se necessário
        subprocess.run([python_bin, "-m", "pip", "install", "--upgrade", "pip", "pipreqs"], check=True)

        # Gerar novo requirements.txt
        subprocess.run([
            python_bin, "-m", "pipreqs", ".", "--force", "--encoding", "utf-8"
        ], check=True)

        print(Fore.GREEN + "[✔] requirements.txt atualizado com sucesso!")
    except subprocess.SubprocessError as e:
        log_error(f"Erro atualizando dependências: {e}")
        print(Fore.RED + f"Erro: {e}")

    input(Fore.YELLOW + "Pressione Enter para voltar...")

def main_menu(user_language: str) -> None:
    """Exibe o menu principal."""
    while True:
        clear_console()
        print(Fore.YELLOW + Style.BRIGHT + " Menu Principal ".center(50, "-"))
        print("1. Atualizar Ferramenta")
        print("2. Atualizar Dependências")
        print("3. Ver Logs de Erro")
        print("0. Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == '0':
            goodbye_message(user_language)
            break
        elif choice == '1':
            update_tool_from_github()
        elif choice == '2':
            update_dependencies_crossplatform()
        elif choice == '3':
            view_logs()
        else:
            handle_invalid_option(user_language)

def main() -> None:
    """Função principal."""
    ensure_admin_privileges()
    init(autoreset=True)
    clear_console()

    args = sys.argv[1:]
    if "--update-tool" in args:
        update_tool_from_github()
        return
    if "--update-dependencies" in args:
        update_dependencies_crossplatform()
        return

    # Seleção de idioma
    print(Fore.YELLOW + " Language Selection ".center(50, "-"))
    print("1. English")
    print("2. Português")
    language_option = input("Choose your language: ").strip()
    user_language = language_option if language_option in ('1', '2') else LANGUAGE_EN

    welcome_message(user_language)
    main_menu(user_language)

if __name__ == "__main__":
    main()
