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
    """Menu completo de gerenciamento VPN"""
    lang = LANGUAGES[user_language]['vpn']

    def mostrar_status() -> str:
        """Exibe o status atual da VPN"""
        if not VPNManager.verificar_instalacao():
            return f"{Fore.RED}✖ {lang['not_installed']}"

        success, status_msg = VPNManager.status()
        if not success:
            return f"{Fore.RED}✖ {status_msg}"

        return (f"{Fore.GREEN}✔ CONECTADO" if "Connected" in status_msg
                else f"{Fore.RED}✖ DESCONECTADO")

    def mostrar_progresso():
        """Exibe uma animação de progresso"""
        for i in range(3):
            print(".", end='', flush=True)
            time.sleep(0.5)
        print()

    def configurar_login() -> bool:
        """Fluxo de login completo"""
        tentativas = 3
        while tentativas > 0:
            clear_console()
            print(f"\n{Fore.YELLOW}▶ Configuração de Login ({tentativas} tentativas restantes)")
            print(f"{Fore.CYAN}▶ Certifique-se de ter uma conexão com a internet estável\n")

            username = input(f"{Fore.CYAN}• Usuário ProtonVPN: ").strip()
            if not username:
                print(f"{Fore.RED}✖ O usuário não pode estar vazio")
                tentativas -= 1
                time.sleep(1)
                continue

            password = input(f"{Fore.CYAN}• Senha ProtonVPN: ").strip()
            if not password:
                print(f"{Fore.RED}✖ A senha não pode estar vazia")
                tentativas -= 1
                time.sleep(1)
                continue

            print(f"\n{Fore.YELLOW}▶ Verificando credenciais", end='')
            mostrar_progresso()

            success, message = VPNManager.login(username, password)
            if success:
                print(f"{Fore.GREEN}✓ {message}")
                return True
            else:
                print(f"{Fore.RED}✖ {message}")
                tentativas -= 1
                if tentativas > 0:
                    input(lang['press_enter'])

        print(f"{Fore.RED}✖ Número máximo de tentativas excedido")
        return False

    def instalar_vpn():
        """Fluxo completo de instalação"""
        print(f"\n{Fore.YELLOW}▶ Iniciando instalação do ProtonVPN...")
        success, message = VPNManager.instalar()
        if success:
            print(f"{Fore.GREEN}✓ {message}")
            if not configurar_login():
                print(f"{Fore.RED}✖ Falha na configuração inicial")
        else:
            print(f"{Fore.RED}✖ {message}")
        input(lang['press_enter'])

    def desinstalar_vpn():
        """Fluxo completo de desinstalação"""
        print(f"\n{Fore.YELLOW}▶ Preparando desinstalação...")
        success, message = VPNManager.desinstalar()
        if success:
            print(f"{Fore.GREEN}✓ {message}")
        else:
            print(f"{Fore.RED}✖ {message}")
        input(lang['press_enter'])

    def verificar_atualizacoes():
        """Verifica por atualizações disponíveis"""
        print(f"\n{Fore.YELLOW}▶ Verificando atualizações...")
        success, message = VPNManager.verificar_atualizacoes()
        if success:
            print(f"{Fore.GREEN}✓ {message}")
            instalar = input("Deseja instalar a atualização? (s/n): ").lower()
            if instalar == 's':
                instalar_vpn()
        else:
            print(f"{Fore.YELLOW}→ {message}")
        input(lang['press_enter'])

    while True:
        clear_console()
        print(f"\n{Fore.YELLOW}╔{'═'*40}╗")
        print(f"║{Fore.CYAN}{'PAINEL DE CONTROLE VPN'.center(40)}{Fore.YELLOW}║")
        print(f"╠{'═'*40}╣")
        print(f"║ Status: {mostrar_status().ljust(32)}║")
        print(f"╠{'═'*40}╣")

        opcoes = [
            ("1", lang['connect']),
            ("2", lang['disconnect']),
            ("3", lang['status']),
            ("4", "Instalar VPN"),
            ("5", "Desinstalar VPN"),
            ("6", "Verificar Atualizações"),
            ("0", lang['back'])
        ]

        for opt, texto in opcoes:
            print(f"║ {Fore.CYAN}{opt}. {texto.ljust(36)}{Fore.YELLOW}║")
        print(f"╚{'═'*40}╝")

        escolha = input(f"\n{Fore.CYAN}▶ Selecione uma opção: ").strip()

        if escolha == "1":  # Conectar
            if not VPNManager.verificar_instalacao():
                print(f"{Fore.RED}✖ ProtonVPN não está instalado")
                input(lang['press_enter'])
                continue

            print(f"{Fore.YELLOW}▶ Conectando ao servidor mais rápido...")
            success, message = VPNManager.conectar()
            print(f"{Fore.GREEN if success else Fore.RED}✓ {message}" if success else f"✖ {message}")
            time.sleep(2)

        elif escolha == "2":  # Desconectar
            print(f"{Fore.YELLOW}▶ Desconectando...")
            success, message = VPNManager.desconectar()
            print(f"{Fore.GREEN if success else Fore.RED}✓ {message}" if success else f"✖ {message}")
            time.sleep(2)

        elif escolha == "3":  # Status
            clear_console()
            print(f"{Fore.YELLOW}▶ Verificando status da VPN...")
            success, message = VPNManager.status()
            if success:
                print(f"\n{Fore.CYAN}{message}")
            else:
                print(f"{Fore.RED}✖ {message}")
            input(lang['press_enter'])

        elif escolha == "4":  # Instalar
            instalar_vpn()

        elif escolha == "5":  # Desinstalar
            desinstalar_vpn()

        elif escolha == "6":  # Verificar atualizações
            verificar_atualizacoes()

        elif escolha == "0":  # Voltar
            break

        else:
            print(f"{Fore.RED}✖ {lang['invalid']}")
            time.sleep(1)

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
            if not VPNManager.verificar_atualizacoes():
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
