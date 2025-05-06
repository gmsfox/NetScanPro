"""
NetScan Pro - Translation Module

This module contains all language strings and translations for the NetScan Pro tool.
It provides multilingual support (English and Portuguese) for all user interface messages.
"""

from colorama import Fore, Style

LANGUAGES = {
    '1': {  # English
        'common': {
            'welcome': f"{Fore.GREEN}{Style.BRIGHT}Welcome to the NetScan Pro tool!",
            'goodbye': f"{Fore.GREEN}{Style.BRIGHT}Thank you for using NetScan Pro!",
            'invalid': f"{Fore.RED}Invalid option. Please try again.",
            'press_enter': "Press Enter to return...",
            'loading': f"{Style.BRIGHT}{Fore.GREEN}GMSFOX",
            'updating': "Updating NetScan Pro...",
            'updated': "Successfully updated!",
            'error': f"{Fore.RED}Error:",
            'no_logs': f"{Fore.YELLOW}No logs found.",
            'requirements_success': f"{Fore.GREEN}[✔] requirements.txt successfully filtered!",
            'requirements_error': f"{Fore.RED}[✘] Error filtering packages:",
            'dependencies_success': f"{Fore.GREEN}[✔] Dependencies updated successfully!",
            'dependencies_error': f"{Fore.RED}[✘] Unexpected error:",
            'select_language': "Choose your language:",
            'language_options': ["1. English", "2. Português"]
        },
        'venv': {
            'error': f"{Fore.RED}Error in venv module:",
            'missing': f"{Fore.YELLOW}Missing venv support. Trying to install...",
            'success': f"{Fore.GREEN}[✔] venv support successfully installed!",
            'fail': f"{Fore.RED}[✘] Failed to install venv:",
            'unsupported': f"{Fore.RED}Automatic installation not supported on this system."
        },
        'admin': {
            'windows': "Restarting as administrator...",
            'linux': "Restarting with sudo..."
        },
        'menu': {
            'title': "Main Menu",
            'options': [
                "Network Tools",
                "Social Engineering Tools",
                "Update Tool",
                "Update Dependencies",
                "VPN",
                "View Logs"
            ],
            'exit': "Exit",
            'choose': "Choose an option: "
        },
        'requirements': {
            'warning': "WARNING: Check these packages in requirements.txt:",
            'package_warn': " → {} (might be a false positive)",
            'check_error': "Error checking requirements:"
        },
        'network': {
            'simulated': "Network tools (simulated)..."
        },
        'social': {
            'simulated': "Social engineering tools (simulated)..."
        },
        'vpn': {
            'menu_title': "PROTONVPN MENU",
            'connect': "Connect VPN",
            'disconnect': "Disconnect VPN",
            'status': "Detailed Status",
            'install': "Install/Update ProtonVPN",
            'back': "Back to Main Menu",
            'connected': "✔ VPN Connected",
            'disconnected': "✖ VPN Disconnected",
            'installing': "Installing ProtonVPN...",
            'updating': "Updating ProtonVPN...",
            'already_installed': "ProtonVPN is already installed.",
            'install_success': "ProtonVPN installed successfully!",
            'install_failed': "ProtonVPN installation failed:",
            'press_enter': "Press Enter to continue...",
            'not_installed': "ProtonVPN is not installed!",
            'install_prompt': "Would you like to install now? (y/n): ",
            'connection_success': "VPN connection established successfully!",
            'connection_failed': "Failed to connect to VPN:",
            'disconnection_success': "VPN disconnected successfully!",
            'disconnection_failed': "Failed to disconnect VPN:",
            'status_checking': "Checking VPN status...",
            'status_connected': "Status: Connected (Secure)",
            'status_disconnected': "Status: Disconnected",
            'installation_instructions': "Please wait while we install ProtonVPN..."
        }
    },
    '2': {  # Português
        'common': {
            'welcome': f"{Fore.GREEN}{Style.BRIGHT}Bem-vindo à ferramenta NetScan Pro!",
            'goodbye': f"{Fore.GREEN}{Style.BRIGHT}Obrigado por usar o NetScan Pro!",
            'invalid': f"{Fore.RED}Opção inválida. Tente novamente.",
            'press_enter': "Pressione Enter para voltar...",
            'loading': f"{Style.BRIGHT}{Fore.GREEN}GMSFOX",
            'updating': "Atualizando o NetScan Pro...",
            'updated': "Atualizado com sucesso!",
            'error': f"{Fore.RED}Erro:",
            'no_logs': f"{Fore.YELLOW}Nenhum log encontrado.",
            'requirements_success': f"{Fore.GREEN}[✔] requirements.txt filtrado com sucesso!",
            'requirements_error': f"{Fore.RED}[✘] Erro ao filtrar pacotes:",
            'dependencies_success': f"{Fore.GREEN}[✔] Dependências atualizadas com sucesso!",
            'dependencies_error': f"{Fore.RED}[✘] Erro inesperado:",
            'select_language': "Escolha seu idioma:",
            'language_options': ["1. Inglês", "2. Português"]
        },
        'venv': {
            'error': f"{Fore.RED}Erro no módulo venv:",
            'missing': f"{Fore.YELLOW}Suporte a venv ausente. Tentando instalar...",
            'success': f"{Fore.GREEN}[✔] Suporte a venv instalado com sucesso!",
            'fail': f"{Fore.RED}[✘] Falha ao instalar venv:",
            'unsupported': f"{Fore.RED}Instalação automática não suportada neste sistema."
        },
        'admin': {
            'windows': "Reiniciando como administrador...",
            'linux': "Reiniciando com sudo..."
        },
        'menu': {
            'title': "Menu Principal",
            'options': [
                "Ferramentas de Rede",
                "Ferramentas de Engenharia Social",
                "Atualizar Ferramenta",
                "Atualizar Dependências",
                "VPN",
                "Ver Logs"
            ],
            'exit': "Sair",
            'choose': "Escolha uma opção: "
        },
        'requirements': {
            'warning': "AVISO: Verifique estes pacotes no requirements.txt:",
            'package_warn': " → {} (pode ser um falso positivo)",
            'check_error': "Erro na verificação de requirements:"
        },
        'network': {
            'simulated': "Ferramentas de rede (simulado)..."
        },
        'social': {
            'simulated': "Ferramentas de engenharia social (simulado)..."
        },
        'vpn': {
            'menu_title': "MENU PROTONVPN",
            'connect': "Conectar VPN",
            'disconnect': "Desconectar VPN",
            'status': "Status Detalhado",
            'install': "Instalar/Atualizar ProtonVPN",
            'back': "Voltar ao Menu Principal",
            'connected': "✔ VPN Conectada",
            'disconnected': "✖ VPN Desconectada",
            'installing': "Instalando ProtonVPN...",
            'updating': "Atualizando ProtonVPN...",
            'already_installed': "ProtonVPN já está instalado.",
            'install_success': "ProtonVPN instalado com sucesso!",
            'install_failed': "Falha na instalação do ProtonVPN:",
            'press_enter': "Pressione Enter para continuar...",
            'not_installed': "ProtonVPN não está instalado!",
            'install_prompt': "Deseja instalar agora? (s/n): ",
            'connection_success': "Conexão VPN estabelecida com sucesso!",
            'connection_failed': "Falha ao conectar à VPN:",
            'disconnection_success': "VPN desconectada com sucesso!",
            'disconnection_failed': "Falha ao desconectar VPN:",
            'status_checking': "Verificando status da VPN...",
            'status_connected': "Status: Conectado (Seguro)",
            'status_disconnected': "Status: Desconectado",
            'installation_instructions': "Por favor aguarde enquanto instalamos o ProtonVPN..."
        }
    }
}
