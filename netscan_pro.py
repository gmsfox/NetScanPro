"""NetScan Pro - Ferramenta de análise de rede.
Ferramenta de rede com funcionalidades de escaneamento e engenharia social.
"""

import os
import platform
import subprocess
import venv
import time
import sys
import logging
import ctypes
from colorama import init, Fore, Style
# Módulos internos
from Tools.vpn_tor.manager import VPNTorManager
from Tools.vpn_tor.installer import VPNTorInstaller
from core.updates import update_dependencies_crossplatform

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
    """Verificação de admin universal que não depende de getuid/geteuid."""
    try:
        if platform.system() == "Windows":
            # Windows: usando API nativa
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print(f"{Fore.YELLOW}Reiniciando como administrador...")
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit(0)
        else:
            # Unix/Linux/Mac: usando tentativa de escrita em /root
            try:
                with open("/root/.test", "w", encoding="utf-8") as f:
                    f.write("test")
                os.unlink("/root/.test")
            except (IOError, OSError):
                print(f"{Fore.YELLOW}Reiniciando com sudo...")
                subprocess.run(["sudo", sys.executable] + sys.argv, check=True)
                sys.exit(0)
    except Exception as e:  # pylint: disable=broad-except
        log_error(f"Falha na elevação: {str(e)}")
        print(f"{Fore.RED}Erro: {str(e)}")
        sys.exit(1)

def ensure_venv_support() -> None:
    """Garante que o suporte a venv está disponível."""
    try:
        # Verifica se o módulo venv está realmente funcional
        if not hasattr(venv, 'EnvBuilder') or not callable(venv.EnvBuilder):
            raise AttributeError("Módulo venv incompleto")

        # Testa criação dummy de ambiente (sem realmente criar)
        dummy_builder = venv.EnvBuilder(with_pip=False)
        if not isinstance(dummy_builder, venv.EnvBuilder):
            raise RuntimeError("Falha na inicialização do venv")

    except (AttributeError, RuntimeError) as e:
        print(f"{Fore.RED}Erro no módulo venv: {e}")
        if platform.system() == "Linux":
            print(f"{Fore.YELLOW}Tentando instalar python3-venv...")
            try:
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "python3-venv"], check=True)
                print(f"{Fore.GREEN}[✔] Suporte a venv instalado com sucesso.")
                # Verifica novamente após instalação
                ensure_venv_support()
                return
            except subprocess.SubprocessError as subprocess_err:
                log_error(f"Falha ao instalar python3-venv: {subprocess_err}")
                print(f"{Fore.RED}Erro ao instalar venv: {subprocess_err}")
            sys.exit(1)
        else:
            print(f"{Fore.RED}Instalação automática não suportada neste sistema.")
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
    msg = ("Welcome to the NetScan Pro tool!"
           if user_language == LANGUAGE_EN else
           "Bem-vindo à ferramenta NetScan Pro!")
    print(f"{Fore.GREEN}{Style.BRIGHT}{msg.center(50)}")

@auto_clear
def goodbye_message(user_language: str) -> None:
    """Mensagem de despedida."""
    msg =("Thank you for using NetScan Pro!"
          if user_language == LANGUAGE_EN else
          "Obrigado por usar o NetScan Pro!")
    print(f"{Fore.GREEN}{Style.BRIGHT}{msg.center(50)}")

@auto_clear
def handle_invalid_option(user_language: str) -> None:
    """Mensagem para opções inválidas."""
    msg =("Invalid option. Please try again."
          if user_language == LANGUAGE_EN else
          "Opção inválida. Tente novamente.")
    print(f"{Fore.RED}{msg}")

@auto_clear
def loading_screen() -> None:
    """Tela de carregamento."""
    print(f"{Style.BRIGHT}{Fore.GREEN}GMSFOX".center(60))

def open_new_terminal(option: str) -> None:
    """Abre nova janela de terminal."""
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["cmd", "/k", f"python {sys.argv[0]} --{option}"])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {sys.argv[0]} --{option}"])
    except subprocess.SubprocessError as e:
        log_error(f"Erro abrindo novo terminal: {e}")
        print(f"{Fore.RED}Erro: {e}")

def view_logs() -> None:
    """Exibe os logs de erro."""
    clear_console()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            print(file.read())
    else:
        print(f"{Fore.YELLOW}Nenhum log encontrado.")
    input(f"{Fore.YELLOW}Pressione Enter para voltar...")

def limpar_requirements(caminho_arquivo="requirements.txt") -> None:
    """Remove pacotes inválidos/obsoletos do arquivo requirements.txt."""
    pacotes_invalidos = {
        '__builtin__', '__pypy__', '_abcoll', '_cmsgpack', '_typeshed', '_winreg',
        'htmlentitydefs', 'httplib', 'Queue', 'StringIO', 'urlparse', 'xmlrpclib',
        'dummy_thread', 'ntlm', 'java', 'js', 'pyodide', 'thread', 'urllib2', 'tomllib',
        'attr', 'brotli', 'ctags', 'ConfigParser', 'HTMLParser'
    }

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]

        pacotes_validos = []
        vistos = set()
        for linha in linhas:
            nome = linha.split("==")[0].split("[")[0].strip()
            if nome not in pacotes_invalidos and nome not in vistos:
                pacotes_validos.append(linha)
                vistos.add(nome)

        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(sorted(pacotes_validos)) + "\n")

        print(f"{Fore.GREEN}[✔] requirements.txt filtrado com sucesso!")
    except (OSError, UnicodeDecodeError) as erro:
        log_error(f"Erro ao limpar requirements.txt: {erro}")
        print(f"{Fore.RED}[✘] Erro ao filtrar pacotes: {erro}")

def verificar_requirements() -> None:
    """Alertas para pacotes que podem exigir revisão manual."""
    suspeitos = [
        "brotlicffi", "chardet", "docutils", "filelock", "h2",
        "ipython", "jnius", "keyring", "protobuf", "zstandard"
    ]

    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            pacotes = [linha.split("==")[0] for linha in f.readlines()]

        alertas = [pkg for pkg in suspeitos if pkg in pacotes]
        if alertas:
            print(f"{Fore.YELLOW}AVISO: Verifique estes pacotes no requirements.txt:")
            for pkg in alertas:
                print(f"{Fore.YELLOW} → {pkg} (pode ser um falso positivo)")
    except (ValueError, UnicodeDecodeError) as e:
        log_error(f"Erro na verificação de requirements: {str(e)}")

def update_tool_from_github() -> None:
    """Atualiza o projeto via GitHub."""
    clear_console()
    print(f"{Fore.YELLOW}Atualizando o NetScan Pro...")
    try:
        subprocess.run(["git", "pull", "https://github.com/gmsfox/NetScanPro.git"], check=True)
        print(f"{Fore.GREEN}Atualizado com sucesso!")
    except subprocess.SubprocessError as e:
        log_error(f"Erro ao atualizar ferramenta: {e}")
        print(f"{Fore.RED}Erro: {e}")
    input(f"{Fore.YELLOW}Pressione Enter para voltar...")

def find_venv_python_executable(venv_path: str) -> str:
    """Procura automaticamente o executável Python dentro da venv."""
    possible_paths = [
        os.path.join(venv_path, "bin", "python3"),
        os.path.join(venv_path, "bin", "python"),
        os.path.join(venv_path, "Scripts", "python.exe"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    for root, _, files in os.walk(venv_path):
        for file in files:
            if file.startswith("python") and os.access(os.path.join(root, file), os.X_OK):
                return os.path.join(root, file)

    raise FileNotFoundError(f"Executável do ambiente virtual não encontrado: {venv_path}")

def vpn_tor_menu(vpn_manager: VPNTorManager, vpn_installer: VPNTorInstaller, lang: str):
    """Menu dedicado à VPN+TOR com verificação real"""
    while True:
        clear_console()
        print(f"{Fore.CYAN}{'VPN + TOR'.center(50, '=')}")
        print("1. Conectar VPN (+Tor)")
        print("2. Desconectar VPN")
        print("3. Ver Status")
        print("4. Download + Instalação")
        print("0. Voltar")

        choice = input("\n[VPN] Escolha: ")

        if choice == "1":
            try:
                if vpn_manager.connect(use_tor=True):
                    print(f"{Fore.GREEN}Conexão estabelecida com sucesso!")
                else:
                    print(f"{Fore.RED}Falha ao conectar. Verifique se o Tor está instalado.")
            except Exception as e:
                print(f"{Fore.RED}Erro na conexão: {e}")
            input("\nPressione Enter para continuar...")

        elif choice == "2":
            vpn_manager.disconnect()
            input("\nPressione Enter para continuar...")

        elif choice == "3":
            status = "✅ Ativa" if vpn_manager.is_connected else "❌ Inativa"
            tor_status = "✅ Disponível" if vpn_installer.check_installation() else "❌ Não instalado"
            print(f"\nStatus VPN: {status}")
            print(f"Status Tor: {tor_status}")
            input("\nPressione Enter para continuar...")

        elif choice == "4":
            clear_console()
            print(f"{Fore.YELLOW}[*] Iniciando instalação do Tor...")

            if vpn_installer.check_installation():
                print(f"{Fore.BLUE}[!] Tor já está instalado")
            else:
                if vpn_installer.install_all():
                    print(f"{Fore.GREEN}[✔] Instalação concluída com sucesso!")
                else:
                    print(f"{Fore.RED}[✘] Falha na instalação. Verifique os logs.")

            input("\nPressione Enter para continuar...")

        elif choice == "0":
            break

def main_menu(user_language: str) -> None:
    """Exibe o menu principal."""
    vpn_manager = VPNTorManager()
    vpn_installer = VPNTorInstaller()

    while True:
        clear_console()
        print(f"{Fore.YELLOW}{Style.BRIGHT}{'Menu Principal'.center(50, '-')}")
        print("1. Ferramentas de Rede")
        print("2. Ferramentas de Engenharia Social")
        print("3. Atualizar Ferramenta")
        print("4. Atualizar Dependências")
        print("5. VPN + TOR")
        print("6. Ver Logs")
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
            vpn_tor_menu(vpn_manager, vpn_installer, user_language)
        elif choice == '6':
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
        input(f"{Fore.YELLOW}Pressione Enter para sair...")
        return
    if "--social-tools" in args:
        print("Ferramentas de engenharia social (simulado)...")
        input(f"{Fore.YELLOW}Pressione Enter para sair...")
        return
    if "--update-tool" in args:
        update_tool_from_github()
        return
    if "--update-dependencies" in args:
        update_dependencies_crossplatform()
        return

    print(f"{Fore.YELLOW}Language Selection ".center(50, "-"))
    print("1. English")
    print("2. Português")
    language_option = input("Choose your language: ")
    user_language = language_option if language_option in ('1', '2') else LANGUAGE_EN

    welcome_message(user_language)
    loading_screen()
    main_menu(user_language)

if __name__ == "__main__":
    main()