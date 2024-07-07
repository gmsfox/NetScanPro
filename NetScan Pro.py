import os
import subprocess
from colorama import init, Fore, Style
import time
import phonenumbers
from phonenumbers import geocoder, carrier, PhoneNumberType, PhoneNumberFormat

# Função para limpar a tela do console
def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para exibir a mensagem de boas-vindas
def welcome_message(language):
    clear_console()
    if language == '1':
        print(Fore.GREEN + Style.BRIGHT + "Bem-vindo à ferramenta NetScan Pro!".center(50))
    else:
        print(Fore.GREEN + Style.BRIGHT + "Welcome to the NetScan Pro tool!".center(50))
    print()
    time.sleep(2)
    clear_console()

# Função para exibir a mensagem de despedida
def goodbye_message(language):
    clear_console()
    if language == '1':
        print(Fore.GREEN + Style.BRIGHT + "Obrigado por usar a ferramenta NetScan Pro!".center(50))
    else:
        print(Fore.GREEN + Style.BRIGHT + "Thank you for using NetScan Pro tool!".center(50))
    time.sleep(3)
    print()

# Função para lidar com opções inválidas
def handle_invalid_option(language):
    clear_console()
    if language == '1':
        print(Fore.RED + "Opção inválida. Por favor, escolha novamente.")
    else:
        print(Fore.RED + "Invalid option. Please choose again.")
    time.sleep(2)

# Função para escolher o idioma
def choose_language():
    clear_console()
    print(Fore.YELLOW + Style.BRIGHT + " Escolha o Idioma ".center(50, '-'))
    print("1. Português")
    print("2. English")
    choice = input("Escolha o idioma / Choose language: ")
    while choice not in ['1', '2']:
        handle_invalid_option('2')  # Exibe mensagem de opção inválida em inglês
        choice = input("Escolha o idioma / Choose language: ")
    return choice

# Função para exibir o menu principal
def main_menu(language):
    while True:
        clear_console()
        if language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Menu Principal ".center(50, '-'))
            print("1. Ferramentas de Rede")
            print("2. Ferramentas de Engenharia Social")
            print("3. Atualizar Ferramenta do GitHub")
            print("0. Sair")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Main Menu ".center(50, '-'))
            print("1. Network Tools")
            print("2. Social Engineering Tools")
            print("3. Update Tool from GitHub")
            print("0. Exit")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            goodbye_message(language)
            break
        elif choice == '1':
            network_tools_menu(language)
        elif choice == '2':
            social_engineering_tools(language)
        elif choice == '3':
            update_tool_from_github()
        else:
            handle_invalid_option(language)

# Função para o menu de ferramentas de rede
def network_tools_menu(language):
    while True:
        clear_console()
        if language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Ferramentas de Rede ".center(50, '-'))
            print("1. Escanear uma Rede")
            print("2. Escanear a Própria Rede")
            print("3. Escaneamento de Vulnerabilidades")
            print("0. Voltar ao Menu Principal")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Network Tools ".center(50, '-'))
            print("1. Scan a Network")
            print("2. Scan Own Network")
            print("3. Vulnerability Scanning")
            print("0. Back to Main Menu")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            return
        elif choice == '1':
            enter_network(language)
            manual_mode(language)
        elif choice == '2':
            scan_own_network(language)
        elif choice == '3':
            vulnerability_scan_mode(language)
        else:
            handle_invalid_option(language)

# Função para entrar com o nome da rede
def enter_network(language):
    clear_console()
    if language == '1':
        return input("Digite o nome da rede: ")
    else:
        return input("Enter the network name: ")

# Função para o modo manual
def manual_mode(language):
    clear_console()
    if language == '1':
        print("Escanenado rede no modo manual...")
    else:
        print("Scanning network in manual mode...")

    # Lógica para o modo manual (simulado)
    time.sleep(3)
    input("Pressione Enter para continuar...")

# Função para escanear a própria rede
def scan_own_network(language):
    clear_console()
    if language == '1':
        print("Escanenando a própria rede...")
    else:
        print("Scanning own network...")

    # Lógica para escanear a própria rede (simulado)
    time.sleep(3)
    input("Pressione Enter para continuar...")

# Função para o escaneamento de vulnerabilidades
def vulnerability_scan_mode(language):
    clear_console()
    if language == '1':
        print("Escaneamento de vulnerabilidades...")
    else:
        print("Vulnerability scanning...")

    # Lógica para o escaneamento de vulnerabilidades (simulado)
    time.sleep(3)
    input("Pressione Enter para continuar...")

# Função para o menu de ferramentas de engenharia social
def social_engineering_tools(language):
    while True:
        clear_console()
        if language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Ferramentas de Engenharia Social ".center(50, '-'))
            print("1. Informações de Número de Telefone")
            print("2. Phishing")
            print("0. Voltar ao Menu Principal")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Social Engineering Tools ".center(50, '-'))
            print("1. Phone Number Information")
            print("2. Phishing")
            print("0. Back to Main Menu")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            return
        elif choice == '1':
            phone_number_info(language)
        elif choice == '2':
            phishing_menu(language)
        else:
            handle_invalid_option(language)

# Função para o submenu de phishing
def phishing_menu(language):
    while True:
        clear_console()
        if language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Menu de Phishing ".center(50, '-'))
            print("1. Páginas de Logins Falsas")
            print("0. Voltar para Ferramentas de Engenharia Social")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Phishing Menu ".center(50, '-'))
            print("1. Fake Login Pages")
            print("0. Back to Social Engineering Tools")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            return
        elif choice == '1':
            fake_login_pages(language)
        else:
            handle_invalid_option(language)

# Função para as páginas de logins falsas
def fake_login_pages(language):
    clear_console()
    if language == '1':
        print("Escolha um site para clonar para login falso:")
        print("1. Facebook")
        print("2. Google")
        print("3. LinkedIn")
        print("0. Voltar para o Menu de Phishing")
    else:
        print("Choose a website to clone for fake login:")
        print("1. Facebook")
        print("2. Google")
        print("3. LinkedIn")
        print("0. Back to Phishing Menu")

    choice = input("Digite sua escolha: ")

    if choice == '0':
        return
    elif choice in ['1', '2', '3']:
        # Lógica para clonar o site escolhido e capturar as credenciais
        print(f"Cloning website {choice}...")
        time.sleep(3)
        # Lógica para redirecionar para o site oficial e capturar as credenciais digitadas
        print("Redirecting to the official website...")
        time.sleep(2)
        username = input("Enter username/email: ")
        password = input("Enter password: ")

        # Exibindo as credenciais capturadas
        print("Captured credentials:")
        print(f"Username/Email: {username}")
        print(f"Password: {password}")
        time.sleep(3)
    else:
        handle_invalid_option(language)

# Função para obter informações do número de telefone
def phone_number_info(language):
    clear_console()
    if language == '1':
        print("Digite o número de telefone no formato internacional (ex.: +5581994852435):")
    else:
        print("Enter the phone number in international format (e.g., +5581994852435):")

    phone_number = input()

    try:
        numobj = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(numobj):
            location = geocoder.description_for_number(numobj, 'pt_BR' if language == '1' else 'en')
            carrier_name = carrier.name_for_number(numobj, 'pt_BR' if language == '1' else 'en')

            # Montagem do JSON de retorno
            phone_info = {
                "valid": True,
                "number": phone_number,
                "local_format": phonenumbers.format_number(numobj, PhoneNumberFormat.NATIONAL),
                "international_format": phonenumbers.format_number(numobj, PhoneNumberFormat.INTERNATIONAL),
                "country_prefix": "+" + str(numobj.country_code),
                "country_code": numobj.country_code,
                "country_name": geocoder.description_for_number(numobj, 'pt_BR' if language == '1' else 'en'),
                "location": location,
                "carrier": carrier_name,
                "line_type": "mobile" if phonenumbers.number_type(numobj) == PhoneNumberType.MOBILE else "landline"
            }

            # Exibindo informações formatadas
            print("Informações do Número de Telefone:")
            print(phone_info)

        else:
            print("Número de telefone inválido.")
    except phonenumbers.phonenumberutil.NumberParseException:
        print("Erro ao analisar o número de telefone. Certifique-se de usar o formato correto.")

    input("\nPressione Enter para continuar...")

# Função para atualizar a ferramenta do GitHub
def update_tool_from_github():
    clear_console()
    print("Atualizando a ferramenta do GitHub...")
    # Lógica para atualizar a ferramenta do GitHub
    subprocess.run(["git", "pull"])
    print("Ferramenta atualizada com sucesso!")
    input("\nPressione Enter para continuar...")

# Função principal para iniciar o programa
def main():
    init(autoreset=True)  # Inicializa o colorama para redefinir as cores do terminal
    language = choose_language()  # Escolha do idioma

    welcome_message(language)  # Mensagem de boas-vindas
    main_menu(language)  # Menu principal

if __name__ == "__main__":
    main()
