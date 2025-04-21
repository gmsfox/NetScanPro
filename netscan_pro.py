"""NetScan Pro - Ferramenta de análise de rede.
Ferramenta de rede com funcionalidades de escaneamento e engenharia social.
"""

import os
import platform
import subprocess
import time
import sys
import logging
import ctypes
import requests
from colorama import init, Fore, Style

LANGUAGE_EN = '1'
LANGUAGE_PT = '2'

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "error.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(message: str) -> None:
    """Logs error messages to a file."""
    logging.error(message)

def clear_console() -> None:
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_admin_privileges() -> None:
    """Ensures the script is running with administrative privileges."""
    try:
        if platform.system() == "Windows":
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print(f"{Fore.YELLOW}Reiniciando como Administrador no Windows...")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)
        else:
            if hasattr(os, 'geteuid') and os.geteuid() != 0:
                print(f"{Fore.YELLOW}Reiniciando com sudo no Linux...")
                subprocess.run(["sudo", sys.executable] + sys.argv, check=True)
                sys.exit(0)
    except Exception as e:
        log_error(f"Erro ao tentar elevar privilégios: {e}")
        print(f"{Fore.RED}Erro ao tentar elevar privilégios: {e}")
        sys.exit(1)

def auto_clear(func):
    """Decorator to clear console and delay execution."""
    def wrapper(*args, **kwargs):
        clear_console()
        result = func(*args, **kwargs)
        time.sleep(2)
        return result
    return wrapper

@auto_clear
def welcome_message(user_language: str) -> None:
    """Displays welcome message."""
    msg = "Welcome to the NetScan Pro tool!" if user_language == LANGUAGE_EN else "Bem-vindo à ferramenta NetScan Pro!"
    print(f"{Fore.GREEN}{Style.BRIGHT}{msg.center(50)}")

@auto_clear
def goodbye_message(user_language: str) -> None:
    """Displays goodbye message."""
    msg = "Thank you for using NetScan Pro tool!" if user_language == LANGUAGE_EN else "Obrigado por usar a ferramenta NetScan Pro!"
    print(f"{Fore.GREEN}{Style.BRIGHT}{msg.center(50)}")

@auto_clear
def handle_invalid_option(user_language: str) -> None:
    """Handles invalid menu option."""
    msg = "Invalid option. Please choose again." if user_language == LANGUAGE_EN else "Opção inválida. Por favor, escolha novamente."
    print(f"{Fore.RED}{msg}")

@auto_clear
def loading_screen() -> None:
    """Displays loading animation."""
    print(f"{Style.BRIGHT}{'@wbrunnno'.center(60)}")

def open_new_terminal(option: str) -> None:
    """Opens a new terminal window running specific command."""
    try:
        cmd = ["cmd", "/k", f"python {sys.argv[0]} --{option}"] if platform.system() == "Windows" else ["x-terminal-emulator", "-e", f"python3 {sys.argv[0]} --{option}"]
        subprocess.Popen(cmd)
    except subprocess.SubprocessError as e:
        log_error(f"Erro ao abrir novo terminal: {e}")
        print(f"{Fore.RED}Erro ao abrir novo terminal: {e}")

def view_logs() -> None:
    """Displays log file content."""
    clear_console()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Nenhum log de erro encontrado.")
    input("Pressione Enter para voltar...")

def network_tools_menu(user_language: str) -> None:
    """Network tools menu."""
    while True:
        clear_console()
        print(Fore.YELLOW + Style.BRIGHT + " Ferramentas de Rede ".center(50, '-'))
        print("1. Escanear a própria rede")
        print("2. Escanear rede manualmente")
        print("3. Scan de vulnerabilidades")
        print("0. Voltar")
        choice = input("Escolha uma opção: ")
        if choice == '0':
            break
        if choice == '1':
            open_new_terminal("scan-own-network")
        elif choice == '2':
            open_new_terminal("manual-network-scan")
        elif choice == '3':
            open_new_terminal("vulnerability-scan")
        else:
            handle_invalid_option(user_language)

def social_engineering_tools(user_language: str) -> None:
    """Social engineering tools menu."""
    while True:
        clear_console()
        print(Fore.YELLOW + Style.BRIGHT + " Engenharia Social ".center(50, '-'))
        print("1. Consulta de Número de Telefone")
        print("2. Simulação de Phishing")
        print("0. Voltar")
        choice = input("Escolha uma opção: ")
        if choice == '0':
            break
        if choice == '1':
            open_new_terminal("phone-number-info")
        elif choice == '2':
            open_new_terminal("phishing-simulation")
        else:
            handle_invalid_option(user_language)

def update_tool_from_github() -> None:
    """Updates project from GitHub."""
    clear_console()
    print(f"{Fore.YELLOW}{Style.BRIGHT}Atualizando o NetScan Pro...")
    try:
        subprocess.run(["git", "pull", "https://github.com/WeverttonBruno/NetScanPro.git"], check=True)
        print(f"{Fore.GREEN}Atualizado com sucesso!")
    except subprocess.SubprocessError as e:
        log_error(f"Erro ao atualizar ferramenta: {e}")
        print(f"{Fore.RED}Erro: {e}")
    input("Pressione Enter para voltar...")

def update_dependencies_crossplatform() -> None:
    """Updates project dependencies using pipreqs."""
    clear_console()
    print(f"{Fore.YELLOW}{Style.BRIGHT}Atualizando dependências...")
    try:
        subprocess.run(["pipreqs", ".", "--force", "--encoding", "utf-8"], check=True)
        print(f"{Fore.GREEN}[✔] requirements.txt atualizado!")
    except FileNotFoundError:
        print(f"{Fore.RED}pipreqs não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pipreqs"], check=True)
        subprocess.run(["pipreqs", ".", "--force", "--encoding", "utf-8"], check=True)
    except subprocess.SubprocessError as e:
        log_error(f"Erro ao atualizar dependências: {e}")
        print(f"{Fore.RED}Erro: {e}")
    input("Pressione Enter para voltar...")

def main_menu(user_language: str) -> None:
    """Main menu navigation."""
    while True:
        clear_console()
        print(Fore.YELLOW + Style.BRIGHT + " Menu Principal ".center(50, '-'))
        print("1. Ferramentas de Rede")
        print("2. Ferramentas de Engenharia Social")
        print("3. Atualizar Ferramenta")
        print("4. Atualizar Dependências")
        print("5. Ver Logs de Erro")
        print("0. Sair")
        choice = input("Escolha uma opção: ")
        if choice == '0':
            goodbye_message(user_language)
            break
        if choice == '1':
            open_new_terminal("network-tools")
        elif choice == '2':
            open_new_terminal("social-tools")
        elif choice == '3':
            open_new_terminal("update-tool")
        elif choice == '4':
            open_new_terminal("update-dependencies")
        elif choice == '5':
            view_logs()
        else:
            handle_invalid_option(user_language)

def main() -> None:
    """Entry point."""
    ensure_admin_privileges()
    init(autoreset=True)
    clear_console()
    args = sys.argv[1:]

    if '--network-tools' in args:
        network_tools_menu(LANGUAGE_EN)
        return
    if '--social-tools' in args:
        social_engineering_tools(LANGUAGE_EN)
        return
    if '--update-tool' in args:
        update_tool_from_github()
        return
    if '--update-dependencies' in args:
        update_dependencies_crossplatform()
        return
    if '--scan-own-network' in args:
        print("Escaneando própria rede (simulado)...")
        time.sleep(3)
        return
    if '--manual-network-scan' in args:
        print("Escaneando rede manualmente (simulado)...")
        time.sleep(3)
        return
    if '--vulnerability-scan' in args:
        print("Executando scan de vulnerabilidades (simulado)...")
        time.sleep(3)
        return
    if '--phone-number-info' in args:
        print("Consultando informação de número de telefone (simulado)...")
        time.sleep(3)
        return
    if '--phishing-simulation' in args:
        print("Executando simulação de phishing (simulado)...")
        time.sleep(3)
        return

    print(Fore.YELLOW + Style.BRIGHT + " Language Selection ".center(50, '-'))
    print("1. English")
    print("2. Português")
    language_option = input("Choose your language: ")
    user_language = language_option if language_option in ('1', '2') else LANGUAGE_EN
    welcome_message(user_language)
    loading_screen()
    main_menu(user_language)

if __name__ == "__main__":
    main()
