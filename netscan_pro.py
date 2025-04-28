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
    """Grava mensagens de erro em arquivo."""
    logging.error(message)

def clear_console() -> None:
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_admin_privileges() -> None:
    """Garante que está rodando como administrador."""
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
                subprocess.run(["sudo", sys.executable] + sys.argv, check=True)
                sys.exit(0)
    except Exception as e:
        log_error(f"Erro ao tentar elevar privilégios: {e}")
        print(Fore.RED + f"Erro: {e}")
        sys.exit(1)

def ensure_venv_support() -> None:
    """Garante que o suporte a ambientes virtuais (venv) está disponível e funcional."""
    temp_venv_path = ".temp_venv_test"

    try:
        subprocess.run([sys.executable, "-m", "venv", temp_venv_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Se chegou aqui, venv está funcionando
        if os.path.exists(temp_venv_path):
            subprocess.run(["rm", "-rf", temp_venv_path], check=False)  # Remove o venv de teste no Linux
    except subprocess.SubprocessError:
        print(Fore.RED + "Ambiente virtual (venv) não funcional. Tentando instalar automaticamente...")
        try:
            if platform.system() == "Linux":
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "python3-venv"], check=True)
                print(Fore.GREEN + "Pacote python3-venv instalado com sucesso!")
            else:
                print(Fore.RED + "Instalação automática de venv não suportada neste sistema.")
                input(Fore.YELLOW + "Pressione Enter para sair...")
                sys.exit(1)
        except subprocess.SubprocessError as install_error:
            log_error(f"Erro instalando python3-venv: {install_error}")
            print(Fore.RED + f"Erro instalando python3-venv: {install_error}")
            input(Fore.YELLOW + "Pressione Enter para sair...")
            sys.exit(1)

def auto_clear(func):
    """Decorator que limpa a tela antes de executar funções."""
    def wrapper(*args, **kwargs):
        clear_console()
        result = func(*args, **kwargs)
        time.sleep(2)
        return result
    return wrapper

@auto_clear
def welcome_message(user_language: str) -> None:
    """Mensagem de boas-vindas."""
    msg = "Welcome to the NetScan Pro tool!" if user_language == LANGUAGE_EN else "Bem-vindo à ferramenta NetScan Pro!"
    print(Fore.GREEN + Style.BRIGHT + msg.center(50))

@auto_clear
def goodbye_message(user_language: str) -> None:
    """Mensagem de despedida."""
    msg = "Thank you for using NetScan Pro!" if user_language == LANGUAGE_EN else "Obrigado por usar o NetScan Pro!"
    print(Fore.GREEN + Style.BRIGHT + msg.center(50))

@auto_clear
def handle_invalid_option(user_language: str) -> None:
    """Mensagem para opções inválidas."""
    msg = "Invalid option. Please try again." if user_language == LANGUAGE_EN else "Opção inválida. Tente novamente."
    print(Fore.RED + msg)

@auto_clear
def loading_screen() -> None:
    """Tela de carregamento."""
    print(Style.BRIGHT + "GMSFOX".center(60))

def open_new_terminal(option: str) -> None:
    """Abre nova janela de terminal."""
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["cmd", "/k", f"python {sys.argv[0]} --{option}"])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {sys.argv[0]} --{option}"])
    except subprocess.SubprocessError as e:
        log_error(f"Erro abrindo novo terminal: {e}")
        print(Fore.RED + f"Erro: {e}")

def view_logs() -> None:
    """Exibe os logs de erro."""
    clear_console()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            print(file.read())
    else:
        print(Fore.YELLOW + "Nenhum log encontrado.")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def limpar_requirements(caminho_arquivo="requirements.txt") -> None:
    """Limpa e organiza o arquivo requirements.txt removendo pacotes desnecessários."""
    pacotes_invalidos = {
        '__builtin__', '__pypy__', '_abcoll', '_cmsgpack', '_typeshed', '_winreg',
        'htmlentitydefs', 'httplib', 'Queue', 'StringIO', 'urlparse', 'xmlrpclib',
        'dummy_thread', 'ntlm', 'java', 'js', 'pyodide', 'thread', 'urllib2',
        'ctags', 'tomllib'
    }

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        pacotes_validos = []
        vistos = set()

        for linha in linhas:
            pacote = linha.strip()
            if not pacote:
                continue
            nome = pacote.split("==")[0] if "==" in pacote else pacote
            if nome not in pacotes_invalidos and nome not in vistos:
                pacotes_validos.append(pacote)
                vistos.add(nome)

        pacotes_validos.sort()

        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(pacotes_validos) + "\n")

        print(Fore.GREEN + "[✔] requirements.txt limpo e atualizado com sucesso!")
    except Exception as erro:
        log_error(f"Erro ao limpar requirements.txt: {erro}")
        print(Fore.RED + f"[✘] Erro ao limpar requirements.txt: {erro}")

def update_tool_from_github() -> None:
    """Atualiza o projeto via GitHub."""
    clear_console()
    print(Fore.YELLOW + "Atualizando o NetScan Pro...")
    try:
        subprocess.run(["git", "pull", "https://github.com/gmsfox/NetScanPro.git"], check=True)
        print(Fore.GREEN + "Atualizado com sucesso!")
    except subprocess.SubprocessError as e:
        log_error(f"Erro ao atualizar ferramenta: {e}")
        print(Fore.RED + f"Erro: {e}")
    input(Fore.YELLOW + "Pressione Enter para voltar...")

def update_dependencies_crossplatform() -> None:
    """Atualiza dependências e gera requirements.txt de forma segura e inteligente."""
    clear_console()
    print(Fore.YELLOW + "Atualizando dependências...")

    venv_path = ".venv"

    try:
        ensure_venv_support()

        if not os.path.exists(venv_path):
            print(Fore.CYAN + "Criando ambiente virtual (.venv)...")
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

        # Define o python_bin
        python_bin = (
            os.path.join(venv_path, "Scripts", "python.exe")
            if platform.system() == "Windows"
            else os.path.join(venv_path, "bin", "python3")
        )

        # Aguarda o python_bin aparecer
        for _ in range(5):
            if os.path.exists(python_bin):
                break
            print(Fore.YELLOW + "Aguardando criação do ambiente virtual...")
            time.sleep(1)
        else:
            raise FileNotFoundError(f"Python virtual environment executable not found: {python_bin}")

        print(Fore.CYAN + "Instalando/Atualizando pipreqs...")
        subprocess.run([python_bin, "-m", "pip", "install", "--upgrade", "pipreqs"], check=True)

        print(Fore.CYAN + "Gerando requirements.txt...")
        subprocess.run([python_bin, "-m", "pipreqs", ".", "--force", "--encoding", "utf-8"], check=True)

        limpar_requirements()

        print(Fore.GREEN + "[✔] requirements.txt atualizado com sucesso!")

    except Exception as e:
        log_error(f"Erro atualizando dependências: {e}")
        print(Fore.RED + f"[✘] Erro ao atualizar dependências: {e}")

    input(Fore.YELLOW + "Pressione Enter para voltar ao menu...")

def main_menu(user_language: str) -> None:
    """Exibe o menu principal."""
    while True:
        clear_console()
        print(Fore.YELLOW + Style.BRIGHT + " Menu Principal ".center(50, "-"))
        print("1. Ferramentas de Rede")
        print("2. Ferramentas de Engenharia Social")
        print("3. Atualizar Ferramenta")
        print("4. Atualizar Dependências")
        print("5. Ver Logs")
        print("0. Sair")
        choice = input("Escolha uma opção: ")
        if choice == '0':
            goodbye_message(user_language)
            break
        elif choice == '1':
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
    """Ponto de entrada principal."""
    ensure_admin_privileges()
    init(autoreset=True)
    clear_console()
    args = sys.argv[1:]

    if "--network-tools" in args:
        print("Ferramentas de rede (simulado)...")
        input(Fore.YELLOW + "Pressione Enter para sair...")
        return
    if "--social-tools" in args:
        print("Ferramentas de engenharia social (simulado)...")
        input(Fore.YELLOW + "Pressione Enter para sair...")
        return
    if "--update-tool" in args:
        update_tool_from_github()
        return
    if "--update-dependencies" in args:
        update_dependencies_crossplatform()
        return

    print(Fore.YELLOW + " Language Selection ".center(50, "-"))
    print("1. English")
    print("2. Português")
    language_option = input("Choose your language: ")
    user_language = language_option if language_option in ('1', '2') else LANGUAGE_EN

    welcome_message(user_language)
    loading_screen()
    main_menu(user_language)

if __name__ == "__main__":
    main()
