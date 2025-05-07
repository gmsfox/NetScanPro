"""
NetScan Pro - Translation Module

Complete language strings for all tool functionality including VPN module.
"""

from colorama import Fore, Style

LANGUAGES = {
    '1': {  # English
        'common': {
            'welcome': f"{Fore.GREEN}{Style.BRIGHT}Welcome to NetScan Pro!",
            'goodbye': f"{Fore.GREEN}{Style.BRIGHT}Thank you for using NetScan Pro!",
            'invalid': f"{Fore.RED}Invalid option. Please try again.",
            'press_enter': "Press Enter to continue...",
            'loading': f"{Style.BRIGHT}{Fore.GREEN}Initializing...",
            'updating': "Updating tool...",
            'updated': "Update completed successfully!",
            'error': f"{Fore.RED}Error:",
            'no_logs': "No log files found.",
            'requirements_success': f"{Fore.GREEN}Requirements cleaned successfully!",
            'requirements_error': f"{Fore.RED}Error cleaning requirements:",
            'dependencies_success': f"{Fore.GREEN}Dependencies updated!",
            'dependencies_error': f"{Fore.RED}Error updating dependencies:",
            'select_language': "Select language:",
            'language_options': ["1. English", "2. Português"]
        },
        'venv': {
            'error': f"{Fore.RED}Virtual environment error:",
            'missing': f"{Fore.YELLOW}Installing venv support...",
            'success': f"{Fore.GREEN}Venv installed successfully!",
            'fail': f"{Fore.RED}Failed to install venv:",
            'unsupported': f"{Fore.RED}Automatic install not supported on this system."
        },
        'admin': {
            'windows': "Elevating to administrator...",
            'linux': "Restarting with sudo privileges..."
        },
        'menu': {
            'title': "MAIN MENU",
            'options': [
                "Network Tools",
                "Social Engineering Tools",
                "Update Tool",
                "Update Dependencies",
                "VPN",
                "View Logs"
            ],
            'exit': "Exit",
            'choose': "Select an option: "
        },
        'requirements': {
            'warning': f"{Fore.YELLOW}Warning: Review these packages:",
            'package_warn': "→ {} (potential false positive)",
            'check_error': "Error checking requirements:"
        },
        'network': {
            'simulated': "[Network tools simulation]"
        },
        'social': {
            'simulated': "[Social engineering tools simulation]"
        },
        'vpn': {
            'menu_title': "VPN CONTROL PANEL",
            'connect': "Connect to VPN",
            'disconnect': "Disconnect VPN",
            'status': "Connection Status",
            'install': "Reinstall VPN",
            'back': "Back to Main Menu",
            'connected': f"{Fore.GREEN}✔ CONNECTED",
            'disconnected': f"{Fore.RED}✖ DISCONNECTED",
            'installing': f"{Fore.YELLOW}Installing ProtonVPN...",
            'updating': f"{Fore.YELLOW}Updating VPN components...",
            'already_installed': f"{Fore.GREEN}ProtonVPN already installed",
            'install_success': f"{Fore.GREEN}✓ Installation successful!",
            'install_failed': f"{Fore.RED}Installation failed:",
            'not_installed': f"{Fore.YELLOW}ProtonVPN not found. Starting automatic installation...",
            'installation_instructions': f"{Fore.CYAN}This may take a few minutes. Please wait...",
            'install_progress': "Installing step {} of {}...",
            'connection_success': f"{Fore.GREEN}✓ VPN connection established!",
            'connection_failed': f"{Fore.RED}Connection failed:",
            'disconnection_success': f"{Fore.GREEN}✓ Disconnected successfully!",
            'disconnection_failed': f"{Fore.RED}Disconnection failed:",
            'status_checking': f"{Fore.YELLOW}Checking VPN status...",
            'status_connected': f"{Fore.GREEN}✓ Secure Connection",
            'status_disconnected': f"{Fore.RED}No VPN Connection",
            'press_enter': "Press Enter to continue..."
        }
    },
    '2': {  # Português
        'common': {
            'welcome': f"{Fore.GREEN}{Style.BRIGHT}Bem-vindo ao NetScan Pro!",
            'goodbye': f"{Fore.GREEN}{Style.BRIGHT}Obrigado por usar o NetScan Pro!",
            'invalid': f"{Fore.RED}Opção inválida. Tente novamente.",
            'press_enter': "Pressione Enter para continuar...",
            'loading': f"{Style.BRIGHT}{Fore.GREEN}Inicializando...",
            'updating': "Atualizando ferramenta...",
            'updated': "Atualização concluída com sucesso!",
            'error': f"{Fore.RED}Erro:",
            'no_logs': "Nenhum arquivo de log encontrado.",
            'requirements_success': f"{Fore.GREEN}Requisitos limpos com sucesso!",
            'requirements_error': f"{Fore.RED}Erro ao limpar requirements:",
            'dependencies_success': f"{Fore.GREEN}Dependências atualizadas!",
            'dependencies_error': f"{Fore.RED}Erro ao atualizar dependências:",
            'select_language': "Selecione o idioma:",
            'language_options': ["1. Inglês", "2. Português"]
        },
        'venv': {
            'error': f"{Fore.RED}Erro no ambiente virtual:",
            'missing': f"{Fore.YELLOW}Instalando suporte a venv...",
            'success': f"{Fore.GREEN}Venv instalado com sucesso!",
            'fail': f"{Fore.RED}Falha ao instalar venv:",
            'unsupported': f"{Fore.RED}Instalação automática não suportada neste sistema."
        },
        'admin': {
            'windows': "Elevando para administrador...",
            'linux': "Reiniciando com privilégios sudo..."
        },
        'menu': {
            'title': "MENU PRINCIPAL",
            'options': [
                "Ferramentas de Rede",
                "Ferramentas de Eng. Social",
                "Atualizar Ferramenta",
                "Atualizar Dependências",
                "VPN",
                "Ver Logs"
            ],
            'exit': "Sair",
            'choose': "Selecione uma opção: "
        },
        'requirements': {
            'warning': f"{Fore.YELLOW}Aviso: Verifique estes pacotes:",
            'package_warn': "→ {} (possível falso positivo)",
            'check_error': "Erro ao verificar requirements:"
        },
        'network': {
            'simulated': "[Simulação de ferramentas de rede]"
        },
        'social': {
            'simulated': "[Simulação de ferramentas de engenharia social]"
        },
        'vpn': {
            'menu_title': "PAINEL DE CONTROLE VPN",
            'connect': "Conectar à VPN",
            'disconnect': "Desconectar VPN",
            'status': "Status de Conexão",
            'install': "Reinstalar VPN",
            'back': "Voltar ao Menu",
            'connected': f"{Fore.GREEN}✔ CONECTADO",
            'disconnected': f"{Fore.RED}✖ DESCONECTADO",
            'installing': f"{Fore.YELLOW}Instalando ProtonVPN...",
            'updating': f"{Fore.YELLOW}Atualizando componentes VPN...",
            'already_installed': f"{Fore.GREEN}ProtonVPN já instalado",
            'install_success': f"{Fore.GREEN}✓ Instalação concluída!",
            'install_failed': f"{Fore.RED}Falha na instalação:",
            'not_installed': f"{Fore.YELLOW}ProtonVPN não encontrado. Iniciando instalação automática...",
            'installation_instructions': f"{Fore.CYAN}Isso pode levar alguns minutos. Por favor aguarde...",
            'install_progress': "Instalando passo {} de {}...",
            'connection_success': f"{Fore.GREEN}✓ Conexão VPN estabelecida!",
            'connection_failed': f"{Fore.RED}Falha na conexão:",
            'disconnection_success': f"{Fore.GREEN}✓ Desconectado com sucesso!",
            'disconnection_failed': f"{Fore.RED}Falha ao desconectar:",
            'status_checking': f"{Fore.YELLOW}Verificando status da VPN...",
            'status_connected': f"{Fore.GREEN}✓ Conexão Segura",
            'status_disconnected': f"{Fore.RED}Sem conexão VPN",
            'press_enter': "Pressione Enter para continuar..."
        }
    }
}
