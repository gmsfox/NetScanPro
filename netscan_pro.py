"""NetScan Pro - Ferramenta de análise de rede.
Ferramenta de rede com funcionalidades de escaneamento e engenharia social.
"""

import os
import platform
import subprocess
import time
import sys
from typing import Optional, Dict, Any

import requests
from colorama import init, Fore, Style

LANGUAGE_EN = '1'
LANGUAGE_PT = '2'


def clear_console() -> None:
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def auto_clear(func):
    """Decorator to clear console before executing the function and wait after execution."""
    def wrapper(*args, **kwargs):
        clear_console()
        result = func(*args, **kwargs)
        time.sleep(2)
        return result
    return wrapper


@auto_clear
def welcome_message(user_language: str) -> None:
    """Displays a welcome message based on selected language."""
    if user_language == LANGUAGE_EN:
        print(f"{Fore.GREEN}{Style.BRIGHT}{'Welcome to the NetScan Pro tool!'.center(50)}")
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}{'Bem-vindo à ferramenta NetScan Pro!'.center(50)}")


@auto_clear
def goodbye_message(user_language: str) -> None:
    """Displays a goodbye message based on selected language."""
    if user_language == LANGUAGE_EN:
        print(f"{Fore.GREEN}{Style.BRIGHT}{'Thank you for using NetScan Pro tool!'.center(50)}")
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}"
              f"{'Obrigado por usar a ferramenta NetScan Pro!'.center(50)}")


@auto_clear
def handle_invalid_option(user_language: str) -> None:
    """Handles invalid menu option selected by the user."""
    if user_language == LANGUAGE_EN:
        print(f"{Fore.RED}Invalid option. Please choose again.")
    else:
        print(f"{Fore.RED}Opção inválida. Por favor, escolha novamente.")


@auto_clear
def loading_screen() -> None:
    """Displays a loading screen."""
    print(f"{Style.BRIGHT}{'@wbrunnno'.center(60)}")


def open_new_terminal(target: str) -> None:
    """Opens a new terminal running the specified function."""
    if platform.system() == "Windows":
        subprocess.Popen(["cmd", "/k", f"python {sys.argv[0]} {target}"])
    else:
        subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {sys.argv[0]} {target}"])


def phishing_menu(user_language: str) -> None:
    """Simulates a phishing menu (not yet implemented)."""
    clear_console()
    message = (
        "(Phishing menu simulation - feature not implemented yet)"
        if user_language == LANGUAGE_EN else
        "(Simulação de menu de phishing - recurso não implementado ainda)"
    )
    print(message)
    time.sleep(2)


def update_tool_from_github() -> None:
    """Updates the tool from GitHub repository."""
    clear_console()
    print(f"{Fore.YELLOW}{Style.BRIGHT}Updating NetScan Pro tool from GitHub...")
    try:
        subprocess.run([
            "git", "pull", "https://github.com/WeverttonBruno/NetScanPro.git"
        ], check=True)
        print("NetScan Pro tool has been updated successfully!")
        print("Please restart the tool manually.")
        sys.exit(0)
    except subprocess.SubprocessError as e:
        print(f"{Fore.RED}Error updating the tool: {e}")
    time.sleep(3)


def update_dependencies_crossplatform() -> None:
    """Updates the requirements.txt automatically using pipreqs."""
    clear_console()
    print(f"{Fore.YELLOW}{Style.BRIGHT}Atualizando dependências do projeto...")
    try:
        subprocess.run(["pipreqs", ".", "--force", "--encoding", "utf-8"], check=True)
        print(f"{Fore.GREEN}[✔] requirements.txt atualizado com sucesso!")
    except subprocess.SubprocessError as e:
        print(f"{Fore.RED}Erro ao atualizar dependências: {e}")
    time.sleep(3)


def get_choice(prompt: str) -> str:
    """Safely gets user input, defaults to '0' on error."""
    try:
        return input(prompt)
    except (OSError, EOFError):
        return '0'


def main_menu(user_language: str) -> None:
    """Displays the main menu and handles navigation."""
    while True:
        clear_console()
        if user_language == LANGUAGE_EN:
            print(f"{Fore.YELLOW}{Style.BRIGHT}{' Main Menu '.center(50, '-')}")
            print("1. Network Tools")
            print("2. Social Engineering Tools")
            print("3. Update Tool")
            print("4. Update Project Dependencies")
            print("0. Exit")
        else:
            print(f"{Fore.YELLOW}{Style.BRIGHT}{' Menu Principal '.center(50, '-')}")
            print("1. Ferramentas de Rede")
            print("2. Ferramentas de Engenharia Social")
            print("3. Atualizar Ferramenta")
            print("4. Atualizar Dependências do Projeto")
            print("0. Sair")

        choice = get_choice("Choose an option: ")

        if choice == '0':
            goodbye_message(user_language)
            break
        elif choice == '1':
            open_new_terminal("--network-tools")
        elif choice == '2':
            open_new_terminal("--social-tools")
        elif choice == '3':
            update_tool_from_github()
        elif choice == '4':
            update_dependencies_crossplatform()
        else:
            handle_invalid_option(user_language)


def network_tools_menu(user_language: str) -> None:
    """Displays the network tools menu and handles user choices."""
    while True:
        clear_console()
        print(f"{Fore.YELLOW}{Style.BRIGHT}{' Ferramentas de Rede '.center(50, '-')}")
        print("1. Escanear Própria Rede")
        print("2. Escanear Rede Manualmente")
        print("3. Scan de Vulnerabilidades")
        print("0. Voltar")

        choice = get_choice("Escolha uma opção: ")

        if choice == '0':
            break
        elif choice == '1':
            scan_own_network(user_language)
        elif choice == '2':
            manual_mode(user_language)
        elif choice == '3':
            vulnerability_scan_mode(user_language)
        else:
            handle_invalid_option(user_language)


def social_engineering_tools(user_language: str) -> None:
    """Displays social engineering tools menu and handles navigation."""
    while True:
        clear_console()
        print(f"{Fore.YELLOW}{Style.BRIGHT}{' Engenharia Social '.center(50, '-')}")
        print("1. Consulta de Número de Telefone")
        print("2. Phishing Simulation (em breve)")
        print("0. Voltar")

        choice = get_choice("Escolha uma opção: ")

        if choice == '0':
            break
        elif choice == '1':
            phone_number_info(user_language)
        elif choice == '2':
            phishing_menu(user_language)
        else:
            handle_invalid_option(user_language)


def enter_network(user_language: str) -> str:
    """Prompts the user to enter the network name."""
    return input("Digite o nome da rede: ")


def manual_mode(user_language: str) -> None:
    """Simulates scanning a network manually."""
    print("Simulando escaneamento manual da rede...")
    time.sleep(2)


def scan_own_network(user_language: str) -> None:
    """Simulates scanning the user's own network."""
    print("Simulando escaneamento da sua própria rede...")
    time.sleep(2)


def vulnerability_scan_mode(user_language: str) -> None:
    """Simulates a vulnerability scan."""
    print("Simulando scan de vulnerabilidades...")
    time.sleep(2)


def consultar_numero(phone_number: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Consults the NumLookup API to validate a phone number."""
    try:
        response = requests.get(f"https://api.numlookupapi.com/api/validate/{phone_number}?apikey={api_key}")
        return response.json()
    except requests.RequestException:
        return None


def phone_number_info(user_language: str) -> None:
    """Fetches and displays information about a phone number."""
    print("Consulta de número de telefone (simulado)...")
    time.sleep(2)


def main() -> None:
    """Initializes the program and displays the main menu."""
    init(autoreset=True)
    clear_console()

    user_language = None
    args = sys.argv[1:]

    if '--network-tools' in args:
        network_tools_menu(LANGUAGE_EN)
        return
    elif '--social-tools' in args:
        social_engineering_tools(LANGUAGE_EN)
        return

    if '--lang' in args:
        try:
            user_language = args[args.index('--lang') + 1]
        except (IndexError, ValueError):
            user_language = LANGUAGE_EN

    if not user_language:
        user_language = os.getenv("NETSCANPRO_LANG")

    if not user_language:
        user_language = LANGUAGE_PT if platform.system() == 'Linux' else LANGUAGE_EN

    welcome_message(user_language)
    main_menu(user_language)


if __name__ == "__main__":
    main()
