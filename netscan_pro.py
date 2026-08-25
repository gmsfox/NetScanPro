"""
NetScan Pro - Network Analysis Tool.
Ferramenta de rede com funcionalidades de escaneamento e engenharia social.
"""

import os
import platform
import subprocess
import json
import re
import venv
import time
import sys
import logging
import shutil
import threading
from colorama import init, Fore, Style
from languages.translations import LANGUAGES

# Constants
LANGUAGE_EN = '1'
LANGUAGE_PT = '2'

# Global cache for update checks (to avoid blocking)
_update_cache = {
    'tool_updates': None,
    'dependency_updates': None,
    'tool_last_check': 0,
    'dependency_last_check': 0,
    'cache_duration': 30  # Cache for 30 seconds
}

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
    os.system('clear')

def ensure_admin_privileges() -> None:
    """Ensure the application is running with Linux administrator privileges."""
    try:
        current_uid = subprocess.run(
            ["id", "-u"], check=True, capture_output=True, text=True
        ).stdout.strip()
        if current_uid != "0":
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
    """Open a Linux terminal window for a tool menu."""
    try:
        venv_python = os.path.join(".venv", "bin", "python3")
        script_path = os.path.abspath(sys.argv[0])

        terminal_options = [
            (["x-terminal-emulator", "-e"], "x-terminal-emulator"),
            (["xterm", "-e"], "xterm"),
            (["gnome-terminal", "--", "bash", "-c"], "gnome-terminal"),
            (["konsole", "-e"], "konsole"),
            (["xfce4-terminal", "-e"], "xfce4-terminal"),
            (["mate-terminal", "-e"], "mate-terminal"),
            (["kitty"], "kitty"),
            (["alacritty", "-e"], "alacritty"),
        ]

        launched = False
        for cmd_prefix, terminal_name in terminal_options:
            try:
                if shutil.which(terminal_name):
                    full_cmd = cmd_prefix + [f"{venv_python} {script_path} --{option}"]
                    subprocess.Popen(full_cmd)
                    launched = True
                    break
            except (subprocess.SubprocessError, FileNotFoundError):
                continue

        if not launched:
            subprocess.Popen(
                ["bash", "-c", f"{venv_python} {script_path} --{option} &"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    except Exception as e:
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

def check_for_updates() -> bool:
    """Check if there are updates available (uses cache to avoid delays)."""
    global _update_cache
    current_time = time.time()

    # Return cached result if fresh
    if (_update_cache['tool_updates'] is not None and
        current_time - _update_cache['tool_last_check'] < _update_cache['cache_duration']):
        return _update_cache['tool_updates']

    # Return False immediately if cache is being checked
    if _update_cache['tool_updates'] is None:
        _update_cache['tool_updates'] = False
        # Start background check
        thread = threading.Thread(target=_check_tool_updates_background, daemon=True)
        thread.start()

    return _update_cache['tool_updates']

def _check_tool_updates_background():
    """Background thread to check for tool updates."""
    global _update_cache
    try:
        subprocess.run(
            ["git", "fetch", "origin", "main"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5
        )

        local_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()

        remote_commit = subprocess.run(
            ["git", "rev-parse", "origin/main"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()

        _update_cache['tool_updates'] = local_commit != remote_commit and bool(remote_commit)
        _update_cache['tool_last_check'] = time.time()
    except Exception:
        _update_cache['tool_updates'] = False

def check_for_dependency_updates() -> bool:
    """Check if there are dependency updates (uses cache to avoid delays)."""
    global _update_cache
    current_time = time.time()

    # Return cached result if fresh
    if (_update_cache['dependency_updates'] is not None and
        current_time - _update_cache['dependency_last_check'] < _update_cache['cache_duration']):
        return _update_cache['dependency_updates']

    # Return False immediately if cache is being checked
    if _update_cache['dependency_updates'] is None:
        _update_cache['dependency_updates'] = False
        # Start background check
        thread = threading.Thread(target=_check_dependency_updates_background, daemon=True)
        thread.start()

    return _update_cache['dependency_updates']

def _check_dependency_updates_background():
    """Background thread to check for dependency updates."""
    global _update_cache
    try:
        project_dir = os.path.dirname(os.path.abspath(__file__))
        python_bin = os.path.join(
            project_dir,
            ".venv",
            "bin",
            "python"
        )

        if not os.path.exists(python_bin):
            python_bin = sys.executable

        requirements_path = os.path.join(project_dir, "requirements.txt")
        with open(requirements_path, "r", encoding="utf-8") as requirements_file:
            required_packages = {
                re.split(r"[<>=!~;\[]", line.split("#", 1)[0], maxsplit=1)[0]
                .strip()
                .lower()
                .replace("_", "-")
                for line in requirements_file
                if line.strip() and not line.lstrip().startswith("#")
            }

        result = subprocess.run(
            [
                python_bin, "-m", "pip", "list", "--outdated",
                "--format=json", "--disable-pip-version-check"
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            _update_cache['dependency_updates'] = False
            return

        outdated_packages = json.loads(result.stdout)
        relevant_updates = {
            package["name"].lower().replace("_", "-")
            for package in outdated_packages
            if package.get("name")
        } & required_packages

        _update_cache['dependency_updates'] = bool(relevant_updates)
        _update_cache['dependency_last_check'] = time.time()
    except Exception:
        _update_cache['dependency_updates'] = False

def restart_application() -> None:
    """Restart the application to load updated code."""
    time.sleep(1)  # Give user time to read the message
    clear_console()
    print(f"{Fore.CYAN}Reiniciando aplicação para carregar atualizações...")
    time.sleep(2)

    # Get the python executable and script path
    python_exec = sys.executable
    script_path = os.path.abspath(sys.argv[0])

    os.execv(python_exec, [python_exec, script_path])

def update_tool_from_github(user_language: str) -> None:
    """Update the project via GitHub with automatic conflict resolution."""
    clear_console()
    print(f"{Fore.YELLOW}{LANGUAGES[user_language]['common']['updating']}")

    update_successful = False
    try:
        # 1. Limpar arquivos não rastreados (__pycache__, .pyc, etc)
        print(f"{Fore.CYAN}▶ Limpando arquivos temporários...")
        subprocess.run(["git", "clean", "-fd"], check=False, capture_output=True)

        # 2. Salvar mudanças locais (stash)
        print(f"{Fore.CYAN}▶ Salvando mudanças locais...")
        subprocess.run(["git", "stash"], check=False, capture_output=True)

        # 3. Fazer pull
        print(f"{Fore.CYAN}▶ Baixando atualizações...")
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            check=False,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # Check if there were actual updates (not "Already up to date")
            if "Already up to date" not in result.stdout and result.stdout.strip():
                print(f"{Fore.GREEN}✓ {LANGUAGES[user_language]['common']['updated']}")
                print(f"{Fore.CYAN}Recarregando aplicação...")
                update_successful = True
            else:
                print(f"{Fore.CYAN}✓ Ferramenta já está atualizada")
                log_error("Tool already up to date")
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            if "Already up to date" in error_msg:
                print(f"{Fore.CYAN}✓ Ferramenta já está atualizada")
            else:
                print(f"{Fore.YELLOW}⚠ {error_msg}")
                log_error(f"Git pull warning: {error_msg}")
    except subprocess.SubprocessError as e:
        log_error(f"Tool update failed: {e}")
        print(f"{Fore.RED}✘ {LANGUAGES[user_language]['common']['error']} {e}")
    finally:
        if update_successful:
            input(f"{Fore.GREEN}Pressione Enter para reiniciar a aplicação...")
            restart_application()
        else:
            input(LANGUAGES[user_language]['common']['press_enter'])

def find_venv_python_executable(venv_path: str) -> str:
    """Automatically find Python executable within venv."""
    possible_paths = [
        os.path.join(venv_path, "bin", "python3"),
        os.path.join(venv_path, "bin", "python"),
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
    """Install only the Python dependencies missing from the virtual environment."""
    global _update_cache
    clear_console()
    print(f"{Fore.YELLOW}{LANGUAGES[user_language]['common']['updating']}")

    venv_path = ".venv"
    python_bin = os.path.join(venv_path, "bin", "python3")
    update_successful = False
    _update_cache['dependency_updates'] = False
    _update_cache['dependency_last_check'] = time.time()
    try:
        ensure_venv_support(user_language)
        if not os.path.exists(python_bin):
            print(f"{Fore.CYAN}Creating virtual environment (.venv)...")
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

        print(f"{Fore.CYAN}Checking requirements.txt...")
        subprocess.run(
            [python_bin, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )

        print(LANGUAGES[user_language]['common']['dependencies_success'])
        update_successful = True
        _update_cache['dependency_updates'] = False
        _update_cache['dependency_last_check'] = time.time()

    except subprocess.CalledProcessError as e:
        error_msg = f"Subprocess error: {e.stderr.decode().strip() if e.stderr else str(e)}"
        log_error(error_msg)
        print(f"{Fore.RED}[✘] {LANGUAGES[user_language]['common']['error']}: {error_msg}")
    except (OSError, PermissionError, FileNotFoundError) as e:
        log_error(f"Critical error: {str(e)}")
        print(f"{Fore.RED}{LANGUAGES[user_language]['common']['dependencies_error']} {str(e)}")
    finally:
        if update_successful:
            input(LANGUAGES[user_language]['common']['press_enter'])
        else:
            _update_cache['dependency_updates'] = None
            _update_cache['dependency_last_check'] = 0
            input(LANGUAGES[user_language]['common']['press_enter'])

def main_menu(user_language: str) -> None:
    while True:
        clear_console()
        print(f"{Fore.YELLOW}{Style.BRIGHT}{LANGUAGES[user_language]['menu']['title'].center(50, '-')}")

        # Check for updates
        has_tool_updates = check_for_updates()
        has_dependency_updates = check_for_dependency_updates()

        for i, option in enumerate(LANGUAGES[user_language]['menu']['options'], 1):
            # Option 3: Atualizar Ferramenta (tool updates)
            if i == 3:
                if has_tool_updates:
                    print(f"{i}. {Fore.GREEN}{Style.BRIGHT}[ATUALIZAÇÃO DISPONÍVEL]{Style.RESET_ALL} {option}")
                else:
                    print(f"{i}. {Fore.GREEN}{Style.BRIGHT}✓ Ferramenta atualizada{Style.RESET_ALL}")
            # Option 4: Atualizar Dependências (dependency updates)
            elif i == 4:
                if has_dependency_updates:
                    print(f"{i}. {Fore.GREEN}{Style.BRIGHT}[ATUALIZAÇÃO DISPONÍVEL]{Style.RESET_ALL} {option}")
                else:
                    print(f"{i}. {Fore.GREEN}{Style.BRIGHT}✓ Dependências atualizadas{Style.RESET_ALL}")
            else:
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
        elif choice == '5':
            view_logs(user_language)
        elif choice == '0':
            goodbye_message(user_language)
            break
        else:
            handle_invalid_option(user_language)

def main() -> None:
    """Main entry point."""
    if platform.system() != "Linux":
        print("Este aplicativo só pode ser executado em terminais Linux.")
        sys.exit(1)

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
