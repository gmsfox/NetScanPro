"""NetScan Pro - Network Analysis Tool.
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
from languages.translations import LANGUAGES
from Tools.VPN.vpn_manager  import VPNManager

# Constants
LANGUAGE_EN = '1'
LANGUAGE_PT = '2'

# Logging configuration
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "error.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(message: str) -> None:
    """Log error messages to file."""
    logging.error(message)

def clear_console() -> None:
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_admin_privileges() -> None:
    """Universal admin verification."""
    try:
        if platform.system() == "Windows":
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print(f"{Fore.YELLOW}{LANGUAGES[LANGUAGE_EN]['admin']['windows']}")
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit(0)
        else:
            try:
                with open("/root/.test", "w", encoding="utf-8") as f:
                    f.write("test")
                os.unlink("/root/.test")
            except (IOError, OSError):
                print(f"{Fore.YELLOW}{LANGUAGES[LANGUAGE_EN]['admin']['linux']}")
                subprocess.run(["sudo", sys.executable] + sys.argv, check=True)
                sys.exit(0)
    except (OSError, subprocess.SubprocessError) as e:
        log_error(f"Elevation failed: {str(e)}")
        print(f"{Fore.RED}{LANGUAGES[LANGUAGE_EN]['common']['error']} {str(e)}")
        sys.exit(1)

def ensure_venv_support(user_language: str) -> None:
    """Ensure venv support is available."""
    lang = LANGUAGES[user_language]['venv']

    try:
        if not hasattr(venv, 'EnvBuilder') or not callable(venv.EnvBuilder):
            raise AttributeError("Incomplete venv module")

        dummy_builder = venv.EnvBuilder(with_pip=False)
        if not isinstance(dummy_builder, venv.EnvBuilder):
            raise RuntimeError("Venv initialization failed")

    except (AttributeError, RuntimeError) as e:
        print(f"{lang['error']} {e}")
        if platform.system() == "Linux":
            print(lang['missing'])
            try:
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "python3-venv"], check=True)
                print(lang['success'])
                ensure_venv_support(user_language)
                return
            except subprocess.SubprocessError as subprocess_err:
                log_error(f"Failed to install python3-venv: {subprocess_err}")
                print(f"{lang['fail']} {subprocess_err}")
            sys.exit(1)
        else:
            print(lang['unsupported'])
            sys.exit(1)

def auto_clear(func):
    """Decorator to clear screen before executing functions."""
    def wrapper(*args, **kwargs):
        clear_console()
        result = func(*args, **kwargs)
        time.sleep(2)
        return result
    return wrapper

@auto_clear
def welcome_message(user_language: str) -> None:
    """Welcome message."""
    msg = LANGUAGES[user_language]['common']['welcome']
    print(msg.center(50))

@auto_clear
def goodbye_message(user_language: str) -> None:
    """Goodbye message."""
    msg = LANGUAGES[user_language]['common']['goodbye']
    print(msg.center(50))

@auto_clear
def handle_invalid_option(user_language: str) -> None:
    """Invalid option message."""
    print(LANGUAGES[user_language]['common']['invalid'])

@auto_clear
def loading_screen(user_language: str) -> None:
    """Loading screen."""
    print(LANGUAGES[user_language]['common']['loading'].center(60))

def open_new_terminal(option: str) -> None:
    """Open new terminal window."""
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["cmd", "/k", f"python {sys.argv[0]} --{option}"])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {sys.argv[0]} --{option}"])
    except subprocess.SubprocessError as e:
        log_error(f"Error opening new terminal: {e}")
        print(f"{Fore.RED}{LANGUAGES[LANGUAGE_EN]['common']['error']} {e}")

def view_logs(user_language: str) -> None:
    """Display error logs."""
    clear_console()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            print(file.read())
    else:
        print(LANGUAGES[user_language]['common']['no_logs'])
    input(LANGUAGES[user_language]['common']['press_enter'])

def limpar_requirements(user_language: str, caminho_arquivo="requirements.txt") -> None:
    """Remove invalid/obsolete packages from requirements.txt."""
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

        print(LANGUAGES[user_language]['common']['requirements_success'])
    except (OSError, UnicodeDecodeError) as erro:
        log_error(f"Error cleaning requirements.txt: {erro}")
        print(f"{LANGUAGES[user_language]['common']['requirements_error']} {erro}")

def verificar_requirements(user_language: str) -> None:
    """Warnings for packages that may require manual review."""
    suspeitos = [
        "brotlicffi", "chardet", "docutils", "filelock", "h2",
        "ipython", "jnius", "keyring", "protobuf", "zstandard"
    ]

    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            pacotes = [linha.split("==")[0] for linha in f.readlines()]

        alertas = [pkg for pkg in suspeitos if pkg in pacotes]
        if alertas:
            lang = LANGUAGES[user_language]['requirements']
            print(f"{Fore.YELLOW}{lang['warning']}")
            for pkg in alertas:
                print(f"{Fore.YELLOW}{lang['package_warn'].format(pkg)}")
    except (ValueError, UnicodeDecodeError) as e:
        log_error(f"Requirements check error: {str(e)}")
        print(f"{Fore.RED}{LANGUAGES[user_language]['requirements']['check_error']} {str(e)}")

def update_tool_from_github(user_language: str) -> None:
    """Update the project via GitHub."""
    clear_console()
    print(f"{Fore.YELLOW}{LANGUAGES[user_language]['common']['updating']}")
    try:
        subprocess.run(["git", "pull", "https://github.com/gmsfox/NetScanPro.git"], check=True)
        print(f"{Fore.GREEN}{LANGUAGES[user_language]['common']['updated']}")
    except subprocess.SubprocessError as e:
        log_error(f"Tool update failed: {e}")
        print(f"{Fore.RED}{LANGUAGES[user_language]['common']['error']} {e}")
    input(LANGUAGES[user_language]['common']['press_enter'])

def find_venv_python_executable(venv_path: str) -> str:
    """Automatically find Python executable within venv."""
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

    raise FileNotFoundError(f"Virtual environment executable not found: {venv_path}")

def update_dependencies_crossplatform(user_language: str) -> None:
    """Update dependencies automatically with advanced filters."""
    clear_console()
    print(f"{Fore.YELLOW}{LANGUAGES[user_language]['common']['updating']}")

    venv_path = ".venv"
    is_windows = platform.system() == "Windows"
    python_bin = os.path.join(venv_path,
                            "Scripts" if is_windows else "bin",
                            "python.exe" if is_windows else "python3")
    pipreqs_path = os.path.join(venv_path,
                              "Scripts" if is_windows else "bin",
                              "pipreqs.exe" if is_windows else "pipreqs")

    try:
        ensure_venv_support(user_language)
        if not os.path.exists(python_bin):
            print(f"{Fore.CYAN}Creating virtual environment (.venv)...")
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            time.sleep(5)

        print(f"{Fore.CYAN}Installing pipreqs...")
        subprocess.run([python_bin, "-m", "pip", "install", "--upgrade", "pipreqs"], check=True)

        print(f"{Fore.CYAN}Generating requirements.txt...")
        subprocess.run([pipreqs_path, ".", "--force", "--encoding", "utf-8"], check=True)

        limpar_requirements(user_language)
        verificar_requirements(user_language)

        print(LANGUAGES[user_language]['common']['dependencies_success'])
        print(f"{Fore.GREEN}Generated file: {os.path.abspath('requirements.txt')}")

    except subprocess.CalledProcessError as e:
        error_msg = f"Subprocess error: {e.stderr.decode().strip() if e.stderr else str(e)}"
        log_error(error_msg)
        print(f"{Fore.RED}[✘] {LANGUAGES[user_language]['common']['error']}: {error_msg}")
    except (OSError, PermissionError, FileNotFoundError) as e:
        log_error(f"Critical error: {str(e)}")
        print(f"{Fore.RED}{LANGUAGES[user_language]['common']['dependencies_error']} {str(e)}")
    finally:
        input(LANGUAGES[user_language]['common']['press_enter'])

def vpn_menu(user_language: str) -> None:
    """Menu completo de VPN com suporte a GUI e CLI"""
    lang = LANGUAGES[user_language]['vpn']

    def show_status() -> str:
        """Exibe o status com base no cliente instalado"""
        if not VPNManager.check_installation():
            return f"{Fore.RED}✖ {lang['not_installed']}"

        success, status_msg = VPNManager.status()
        if not success:
            return f"{Fore.RED}✖ {status_msg}"

        return (f"{Fore.GREEN}✔ CONECTADO" if "Connected" in status_msg
                else f"{Fore.RED}✖ DESCONECTADO")

    def install_flow() -> bool:
        """Fluxo de instalação completo"""
        print(f"\n{Fore.YELLOW}▶ Iniciando instalação ProtonVPN...")

        # 1. Instalação base
        success, message = VPNManager.install()
        if not success:
            print(f"{Fore.RED}✖ {lang['install_failed']}: {message}")
            return False

        print(f"{Fore.GREEN}✓ {message}")

        # 2. Configuração de login
        print(f"\n{Fore.CYAN}▶ {lang['configuring_login']}")
        username = input(f"{Fore.CYAN}• ProtonVPN Username: ")
        password = input(f"{Fore.CYAN}• ProtonVPN Password: ")

        success, message = VPNManager.login(username, password)
        if not success:
            print(f"{Fore.RED}✖ {lang['login_failed'].format(message)}")
            return False

        print(f"{Fore.GREEN}✓ {lang['login_success']}")
        return True

    while True:
        try:
            clear_console()
            print(f"\n{Fore.YELLOW}╔{'═'*40}╗")
            print(f"║{Fore.CYAN}{'PAINEL DE CONTROLE VPN'.center(40)}{Fore.YELLOW}║")
            print(f"╠{'═'*40}╣")
            print(f"║ Status: {show_status().ljust(32)}║")
            print(f"╠{'═'*40}╣")

            options = [
                ("1", lang['connect']),
                ("2", lang['disconnect']),
                ("3", lang['status']),
                ("4", "Instalar/Reinstalar"),
                ("0", lang['back'])
            ]

            for opt, text in options:
                print(f"║ {Fore.CYAN}{opt}. {text.ljust(36)}{Fore.YELLOW}║")
            print(f"╚{'═'*40}╝")

            choice = input(f"\n{Fore.CYAN}▶ Selecione uma opção: ").strip()

            if choice == "1":  # Conectar
                if not VPNManager.check_installation():
                    if not install_flow():
                        input(lang['press_enter'])
                        continue

                print(f"{Fore.YELLOW}▶ Conectando...")
                success, message = VPNManager.connect()
                print(f"{Fore.GREEN if success else Fore.RED}✓ {message}" if success else f"✖ {message}")
                time.sleep(2)

            elif choice == "2":  # Desconectar
                print(f"{Fore.YELLOW}▶ Desconectando...")
                success, message = VPNManager.disconnect()
                print(f"{Fore.GREEN if success else Fore.RED}✓ {message}" if success else f"✖ {message}")
                time.sleep(2)

            elif choice == "3":  # Status
                clear_console()
                print(f"{Fore.YELLOW}▶ Verificando status...")
                success, message = VPNManager.status()
                if success:
                    print(f"\n{Fore.CYAN}{message}")
                else:
                    print(f"{Fore.RED}✖ {message}")
                input(lang['press_enter'])

            elif choice == "4":  # Instalar/Reinstalar
                print(f"{Fore.YELLOW}▶ Preparando reinstalação...")
                success, message = VPNManager.cleanup()
                if not success:
                    print(f"{Fore.RED}⚠ Aviso na limpeza: {message}")

                if install_flow():
                    print(f"{Fore.GREEN}✓ VPN pronta para uso!")
                input(lang['press_enter'])

            elif choice == "0":  # Voltar
                break

            else:
                print(f"{Fore.RED}✖ {lang['invalid']}")
                time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}← Operação cancelada")
            time.sleep(1)
            break
        except Exception as e:
            print(f"{Fore.RED}⚠ Erro inesperado: {str(e)}")
            logging.error(f"VPN Menu Error: {str(e)}")
            input(lang['press_enter'])

def main_menu(user_language: str) -> None:
    while True:
        clear_console()
        print(f"{Fore.YELLOW}{Style.BRIGHT}{LANGUAGES[user_language]['menu']['title'].center(50, '-')}")
        for i, option in enumerate(LANGUAGES[user_language]['menu']['options'], 1):
            print(f"{i}. {option}")
        print(f"0. {LANGUAGES[user_language]['menu']['exit']}")

        choice = input(LANGUAGES[user_language]['menu']['choose']).strip()

        if choice == '1':
            open_new_terminal("network-tools")
        elif choice == '2':
            open_new_terminal("social-tools")
        elif choice == '3':
            update_tool_from_github(user_language)
        elif choice == '4':
            update_dependencies_crossplatform(user_language)
        elif choice == '5':  # VPN
            if not VPNManager.check_installation():
                print(f"{Fore.RED}ProtonVPN não está instalado!")
                if input("Instalar agora? (s/n): ").lower() == "s":
                    vpn_menu(user_language)
            else:
                vpn_menu(user_language)
        elif choice == '6':
            view_logs(user_language)
        elif choice == '0':
            goodbye_message(user_language)
            break
        else:
            handle_invalid_option(user_language)

def main() -> None:
    """Main entry point."""
    ensure_admin_privileges()
    init(autoreset=True)
    clear_console()
    args = sys.argv[1:]

    if "--network-tools" in args:
        print(f"{Fore.YELLOW}{LANGUAGES[LANGUAGE_EN]['network']['simulated']}")
        input(f"{Fore.YELLOW}{LANGUAGES[LANGUAGE_EN]['common']['press_enter']}")
        return
    if "--social-tools" in args:
        print(f"{Fore.YELLOW}{LANGUAGES[LANGUAGE_EN]['social']['simulated']}")
        input(f"{Fore.YELLOW}{LANGUAGES[LANGUAGE_EN]['common']['press_enter']}")
        return
    if "--update-tool" in args:
        update_tool_from_github(LANGUAGE_PT)
        return
    if "--update-dependencies" in args:
        update_dependencies_crossplatform(LANGUAGE_PT)
        return

    print(f"{Fore.YELLOW}Language Selection ".center(50, "-"))
    for option in LANGUAGES[LANGUAGE_EN]['common']['language_options']:
        print(option)
    language_option = input(LANGUAGES[LANGUAGE_EN]['common']['select_language'] + " ").strip()
    user_language = language_option if language_option in ('1', '2') else LANGUAGE_EN

    welcome_message(user_language)
    loading_screen(user_language)
    main_menu(user_language)

if __name__ == "__main__":
    main()
