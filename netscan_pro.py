"""NetScan Pro - Ferramenta de análise de rede e engenharia social."""

import os
import sys
import platform
import subprocess
import time
import logging
import ctypes
from typing import Optional

import requests
from colorama import init, Fore, Style

# Constantes de idioma
LANGUAGE_EN = '1'
LANGUAGE_PT = '2'

# Configurações de log
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "error.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(message: str) -> None:
    """Registra erro no arquivo de log."""
    logging.error(message)

def clear_console() -> None:
    """Limpa o console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def auto_clear(func):
    """Decorador para limpar o console antes de executar a função."""
    def wrapper(*args, **kwargs):
        clear_console()
        result = func(*args, **kwargs)
        time.sleep(2)
        return result
    return wrapper

def ensure_admin_privileges() -> None:
    """Garante execução como administrador ou sudo."""
    try:
        if platform.system() == "Windows":
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print(Fore.YELLOW + "Reiniciando como Administrador...")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)
        elif hasattr(os, 'geteuid') and os.geteuid() != 0:
            print(Fore.YELLOW + "Reiniciando com sudo...")
            subprocess.run(["sudo", sys.executable] + sys.argv, check=True)
            sys.exit(0)
    except Exception as e:
        log_error(f"Erro elevando privilégios: {e}")
        print(Fore.RED + f"Erro elevando privilégios: {e}")
        sys.exit(1)

@auto_clear
def welcome_message(user_language: str) -> None:
    """Mensagem de boas-vindas."""
    message = "Welcome to NetScan Pro!" if user_language == LANGUAGE_EN else "Bem-vindo ao NetScan Pro!"
    print(Fore.GREEN + Style.BRIGHT + message.center(50))

@auto_clear
def goodbye_message(user_language: str) -> None:
    """Mensagem de despedida."""
    message = "Thank you for using NetScan Pro!" if user_language == LANGUAGE_EN else "Obrigado por usar o NetScan Pro!"
    print(Fore.GREEN + Style.BRIGHT + message.center(50))

@auto_clear
def handle_invalid_option(user_language: str) -> None:
    """Mensagem de opção inválida."""
    message = "Invalid option. Please choose again." if user_language == LANGUAGE_EN else "Opção inválida. Escolha novamente."
    print(Fore.RED + message)

@auto_clear
def loading_screen() -> None:
    """Tela de carregamento."""
    print(Style.BRIGHT + "GMSFOX".center(60))

def open_new_terminal(option: str) -> None:
    """Abre novo terminal com argumento."""
    try:
        cmd = ["cmd", "/k", f"python {sys.argv[0]} --{option}"] if platform.system() == "Windows" else ["x-terminal-emulator", "-e", f"python3 {sys.argv[0]} --{option}"]
        subprocess.Popen(cmd)
    except Exception as e:
        log_error(f"Erro ao abrir terminal: {e}")
        print(Fore.RED + f"Erro: {e}")

def view_logs() -> None:
    """Visualiza logs."""
    clear_console()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Nenhum log encontrado.")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def update_tool_from_github() -> None:
    """Atualiza ferramenta via GitHub."""
    clear_console()
    print(Fore.YELLOW + "Atualizando ferramenta...")
    try:
        subprocess.run(["git", "pull", "https://github.com/WeverttonBruno/NetScanPro.git"], check=True)
        print(Fore.GREEN + "Atualizado com sucesso!")
    except Exception as e:
        log_error(f"Erro atualizando ferramenta: {e}")
        print(Fore.RED + f"Erro: {e}")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def update_dependencies_crossplatform() -> None:
    """Atualiza dependências criando .venv se necessário."""
    clear_console()
    print(Fore.YELLOW + "Atualizando dependências...")

    venv_path = ".venv"
    python_bin = os.path.join(venv_path, "Scripts", "python.exe") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "python")

    try:
        if not os.path.exists(venv_path):
            print(Fore.CYAN + "Criando ambiente virtual...")
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print(Fore.GREEN + "Virtualenv criada!")

        print(Fore.CYAN + "Instalando pipreqs na virtualenv...")
        subprocess.run([python_bin, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([python_bin, "-m", "pip", "install", "pipreqs"], check=True)

        print(Fore.CYAN + "Gerando requirements.txt...")
        subprocess.run([python_bin, "-m", "pipreqs", ".", "--force", "--encoding", "utf-8"], check=True)

        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            print(Fore.GREEN + f"✅ {len(lines)} pacotes adicionados ao requirements.txt!")
        else:
            print(Fore.RED + "requirements.txt não foi gerado!")

    except subprocess.CalledProcessError as e:
        log_error(f"Erro ao atualizar dependências: {e}")
        print(Fore.RED + f"Erro: {e}")

    input(Fore.YELLOW + "Pressione Enter para voltar ao menu...")

def network_tools_menu(user_language: str) -> None:
    """Menu de ferramentas de rede."""
    while True:
        clear_console()
        print(Fore.YELLOW + " Ferramentas de Rede ".center(50, '-'))
        print("1. Escanear própria rede")
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
    """Menu de ferramentas de engenharia social."""
    while True:
        clear_console()
        print(Fore.YELLOW + " Engenharia Social ".center(50, '-'))
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

def main_menu(user_language: str) -> None:
    """Menu principal."""
    while True:
        clear_console()
        print(Fore.YELLOW + " Menu Principal ".center(50, '-'))
        print("1. Ferramentas de Rede")
        print("2. Engenharia Social")
        print("3. Atualizar Ferramenta")
        print("4. Atualizar Dependências")
        print("5. Ver Logs")
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
    """Ponto de entrada."""
    ensure_admin_privileges()
    init(autoreset=True)
    clear_console()
    args = sys.argv[1:]

    if "--network-tools" in args:
        network_tools_menu(LANGUAGE_EN)
        return
    if "--social-tools" in args:
        social_engineering_tools(LANGUAGE_EN)
        return
    if "--update-tool" in args:
        update_tool_from_github()
        return
    if "--update-dependencies" in args:
        update_dependencies_crossplatform()
        return
    if "--scan-own-network" in args:
        print("Simulando escaneamento da própria rede...")
        time.sleep(2)
        return
    if "--manual-network-scan" in args:
        print("Simulando escaneamento manual da rede...")
        time.sleep(2)
        return
    if "--vulnerability-scan" in args:
        print("Simulando scan de vulnerabilidades...")
        time.sleep(2)
        return
    if "--phone-number-info" in args:
        print("Simulando consulta de número de telefone...")
        time.sleep(2)
        return
    if "--phishing-simulation" in args:
        print("Simulando phishing...")
        time.sleep(2)
        return

    # Menu inicial
    print(Fore.YELLOW + " Selecione o idioma ".center(50, '-'))
    print("1. English")
    print("2. Português")
    language_option = input("Escolha seu idioma: ")
    user_language = language_option if language_option in ('1', '2') else LANGUAGE_EN
    welcome_message(user_language)
    loading_screen()
    main_menu(user_language)

if __name__ == "__main__":
    main()
