"""NetScan Pro - Ferramenta de análise de rede.
Ferramenta de rede com funcionalidades de escaneamento e engenharia social.
"""

import os
import platform
import subprocess
import sys
import time
import logging
import ctypes
import requests
from colorama import init, Fore, Style

# Constantes
LANGUAGE_EN = '1'
LANGUAGE_PT = '2'

# Configurar logs
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "error.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(message: str) -> None:
    """Grava erros no arquivo de log."""
    logging.error(message)

def clear_console() -> None:
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_admin_privileges() -> None:
    """Garante privilégios de administrador."""
    try:
        if platform.system() == "Windows":
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print(Fore.YELLOW + "Reiniciando como administrador...")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)
        else:
            if hasattr(os, 'geteuid') and os.geteuid() != 0:
                print(Fore.YELLOW + "Reiniciando com sudo...")
                subprocess.run(["sudo", sys.executable] + sys.argv)
                sys.exit(0)
    except Exception as e:
        log_error(f"Erro elevando privilégios: {e}")
        print(Fore.RED + f"Erro elevando privilégios: {e}")
        sys.exit(1)

def ensure_venv_support() -> None:
    """Garante que o sistema suporte virtualenv."""
    try:
        import venv
    except ImportError:
        print(Fore.RED + "Seu sistema não possui suporte a venv (python3-venv não instalado).")
        print(Fore.YELLOW + "Instale usando: sudo apt install python3-venv")
        input(Fore.YELLOW + "Pressione Enter para sair...")
        sys.exit(1)

def auto_clear(func):
    """Decorador para limpar tela automaticamente."""
    def wrapper(*args, **kwargs):
        clear_console()
        result = func(*args, **kwargs)
        time.sleep(2)
        return result
    return wrapper

@auto_clear
def welcome_message(user_language: str) -> None:
    msg = "Welcome to NetScan Pro!" if user_language == LANGUAGE_EN else "Bem-vindo ao NetScan Pro!"
    print(Fore.GREEN + Style.BRIGHT + msg.center(50))

@auto_clear
def goodbye_message(user_language: str) -> None:
    msg = "Thank you for using NetScan Pro!" if user_language == LANGUAGE_EN else "Obrigado por usar o NetScan Pro!"
    print(Fore.GREEN + Style.BRIGHT + msg.center(50))

@auto_clear
def handle_invalid_option(user_language: str) -> None:
    msg = "Invalid option. Please choose again." if user_language == LANGUAGE_EN else "Opção inválida. Tente novamente."
    print(Fore.RED + msg)

@auto_clear
def loading_screen() -> None:
    print(Style.BRIGHT + "@wbrunnno".center(60))

def open_new_terminal(option: str) -> None:
    """Abre novo terminal para rodar uma função."""
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["cmd", "/k", f"python {sys.argv[0]} --{option}"])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {sys.argv[0]} --{option}"])
    except Exception as e:
        log_error(f"Erro ao abrir terminal: {e}")
        print(Fore.RED + f"Erro ao abrir terminal: {e}")

def view_logs() -> None:
    """Visualiza erros de execução."""
    clear_console()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if content:
                print(content)
            else:
                print(Fore.CYAN + "Nenhum log encontrado.")
    else:
        print(Fore.CYAN + "Nenhum log encontrado.")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def update_tool_from_github() -> None:
    """Atualiza a ferramenta a partir do GitHub."""
    clear_console()
    print(Fore.YELLOW + "Atualizando ferramenta...")
    try:
        subprocess.run(["git", "pull", "https://github.com/WeverttonBruno/NetScanPro.git"], check=True)
        print(Fore.GREEN + "Atualizado com sucesso!")
    except Exception as e:
        log_error(f"Erro ao atualizar ferramenta: {e}")
        print(Fore.RED + f"Erro ao atualizar ferramenta: {e}")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def update_dependencies_crossplatform() -> None:
    """Atualiza dependências com ambiente virtual."""
    clear_console()
    print(Fore.YELLOW + "Atualizando dependências...")
    venv_path = ".venv"
    python_bin = os.path.join(venv_path, "Scripts", "python.exe") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "python3")

    try:
        ensure_venv_support()

        if not os.path.exists(venv_path):
            print(Fore.CYAN + "Criando ambiente virtual...")
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

        print(Fore.CYAN + "Atualizando pip no venv...")
        subprocess.run([python_bin, "-m", "pip", "install", "--upgrade", "pip"], check=True)

        print(Fore.CYAN + "Instalando pipreqs...")
        subprocess.run([python_bin, "-m", "pip", "install", "pipreqs"], check=True)

        print(Fore.CYAN + "Gerando requirements.txt...")
        subprocess.run([python_bin, "-m", "pipreqs", ".", "--force", "--encoding", "utf-8"], check=True)

        print(Fore.GREEN + "✅ Dependências atualizadas com sucesso!")

    except Exception as e:
        log_error(f"Erro atualizando dependências: {e}")
        print(Fore.RED + f"Erro: {e}")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def network_tools_menu(user_language: str) -> None:
    while True:
        clear_console()
        print(Fore.YELLOW + Style.BRIGHT + " Ferramentas de Rede ".center(50, '-'))
        print("1. Escanear Própria Rede")
        print("2. Escanear Manualmente")
        print("3. Scan de Vulnerabilidades")
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
    while True:
        clear_console()
        print(Fore.YELLOW + Style.BRIGHT + " Engenharia Social ".center(50, '-'))
        print("1. Consulta Número de Telefone")
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

def main_menu(user_language: str) -> None:
    while True:
        clear_console()
        print(Fore.YELLOW + Style.BRIGHT + " Menu Principal ".center(50, '-'))
        print("1. Ferramentas de Rede")
        print("2. Engenharia Social")
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
        print("Simulando escaneamento da própria rede...")
        time.sleep(3)
        return
    if '--manual-network-scan' in args:
        print("Simulando escaneamento manual...")
        time.sleep(3)
        return
    if '--vulnerability-scan' in args:
        print("Simulando scan de vulnerabilidades...")
        time.sleep(3)
        return
    if '--phone-number-info' in args:
        print("Simulando consulta de telefone...")
        time.sleep(3)
        return
    if '--phishing-simulation' in args:
        print("Simulando phishing...")
        time.sleep(3)
        return

    print(Fore.YELLOW + Style.BRIGHT + " Selecione o Idioma ".center(50, '-'))
    print("1. English")
    print("2. Português")
    language_option = input("Escolha: ")
    user_language = language_option if language_option in ('1', '2') else LANGUAGE_EN
    welcome_message(user_language)
    loading_screen()
    main_menu(user_language)

if __name__ == "__main__":
    main()
