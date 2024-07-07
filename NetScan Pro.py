import os
import subprocess
from colorama import init, Fore, Style
import time
import shutil
import requests
import zipfile

# URL do seu repositório no GitHub
github_repo_url = "https://github.com/WeverttonBruno/NetScanPro"

# Função para limpar a tela do console
def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para exibir a mensagem de boas-vindas
def welcome_message(language):
    clear_console()
    if language == '1':
        print(Fore.GREEN + Style.BRIGHT + "Welcome to the NetScan Pro tool!".center(50))
    else:
        print(Fore.GREEN + Style.BRIGHT + "Bem-vindo à ferramenta NetScan Pro!".center(50))
    print()
    time.sleep(2)
    clear_console()

# Função para exibir a mensagem de despedida
def goodbye_message(language):
    clear_console()
    if language == '1':
        print(Fore.GREEN + Style.BRIGHT + "Thank you for using NetScan Pro tool!".center(50))
    else:
        print(Fore.GREEN + Style.BRIGHT + "Obrigado por usar a ferramenta NetScan Pro!".center(50))
    time.sleep(3)
    print()

# Função para lidar com opções inválidas
def handle_invalid_option(language):
    clear_console()
    if language == '1':
        print(Fore.RED + "Invalid option. Please choose again.")
    else:
        print(Fore.RED + "Opção inválida. Por favor, escolha novamente.")
    time.sleep(2)

# Função para exibir a mensagem de carregamento
def loading_screen():
    print("Loading...")
    time.sleep(3)
    clear_console()
    print(Style.BRIGHT + "@wbrunnno".center(100))
    time.sleep(1)

# Função para atualizar a ferramenta do GitHub
def update_tool_from_github(language):
    clear_console()
    print(Fore.YELLOW + Style.BRIGHT + "Updating NetScan Pro tool from GitHub...")

    try:
        # Fazendo o download do repositório do GitHub como um arquivo zip temporário
        download_url = github_repo_url + "/archive/refs/heads/main.zip"
        response = requests.get(download_url)
        with open("temp.zip", "wb") as zip_file:
            zip_file.write(response.content)

        # Extraindo o arquivo zip para uma pasta temporária
        with zipfile.ZipFile("temp.zip", "r") as zip_ref:
            zip_ref.extractall("temp_extracted")

        # Copiando os arquivos extraídos para o diretório atual
        repo_folder = os.path.join("temp_extracted", "NetScanPro-main")
        if os.path.exists(repo_folder):
            for item in os.listdir(repo_folder):
                src = os.path.join(repo_folder, item)
                dst = os.path.join(os.getcwd(), item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

        # Removendo arquivos temporários
        shutil.rmtree("temp_extracted")
        os.remove("temp.zip")

        # Reiniciando a ferramenta após a atualização
        print("Restarting NetScan Pro tool...")
        time.sleep(2)
        clear_console()
        print("NetScan Pro tool has been updated and restarted.")

        time.sleep(2)
    except Exception as e:
        print(Fore.RED + f"Error updating the tool: {e}")

    # Retorna ao menu principal após a atualização
    time.sleep(3)
    main_menu(language)

# Função para exibir o menu principal
def main_menu(language):
    while True:
        clear_console()
        if language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Main Menu ".center(50, '-'))
            print("1. Network Tools")
            print("2. Social Engineering Tools")
            print("3. Update Tool")
            print("0. Exit")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Menu Principal ".center(50, '-'))
            print("1. Ferramentas de Rede")
            print("2. Ferramentas de Engenharia Social")
            print("3. Atualizar Ferramenta")
            print("0. Sair")

        choice = input("Choose an option: ")

        if choice == '0':
            goodbye_message(language)
            break
        elif choice == '1':
            network_tools_menu(language)
        elif choice == '2':
            social_engineering_tools(language)
        elif choice == '3':
            update_tool_from_github(language)
        else:
            handle_invalid_option(language)

# Função para o menu de ferramentas de rede
def network_tools_menu(language):
    while True:
        clear_console()
        if language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Network Tools ".center(50, '-'))
            print("1. Scan a Network")
            print("2. Scan Own Network")
            print("3. Vulnerability Scanning")
            print("0. Back to Main Menu")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Ferramentas de Rede ".center(50, '-'))
            print("1. Escanear uma Rede")
            print("2. Escanear a Própria Rede")
            print("3. Escaneamento de Vulnerabilidades")
            print("0. Voltar ao Menu Principal")

        choice = input("Choose an option: ")

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
        return input("Enter the network name: ")
    else:
        return input("Digite o nome da rede: ")

# Função para o modo manual
def manual_mode(language):
    clear_console()
    if language == '1':
        print("Scanning network in manual mode...")
    else:
        print("Escanenado rede no modo manual...")

    # Lógica para o modo manual (simulado)
    time.sleep(3)
    input("Press Enter to continue...")

# Função para escanear a própria rede
def scan_own_network(language):
    clear_console()
    if language == '1':
        print("Scanning own network...")
    else:
        print("Escanenando a própria rede...")

    # Lógica para escanear a própria rede (simulado)
    time.sleep(3)
    input("Press Enter to continue...")

# Função para o escaneamento de vulnerabilidades
def vulnerability_scan_mode(language):
    clear_console()
    if language == '1':
        print("Vulnerability scanning...")
    else:
        print("Escaneamento de vulnerabilidades...")

    # Lógica para o escaneamento de vulnerabilidades (simulado)
    time.sleep(3)
    input("Press Enter to continue...")

# Função para o menu de ferramentas de engenharia social
def social_engineering_tools(language):
    while True:
        clear_console()
        if language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Social Engineering Tools ".center(50, '-'))
            print("1. Phone Number Information")
            print("2. Phishing")
            print("0. Back to Main Menu")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Ferramentas de Engenharia Social ".center(50, '-'))
            print("1. Informações de Número de Telefone")
            print("2. Phishing")
            print("0. Voltar ao Menu Principal")

        choice = input("Choose an option: ")

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
            print(Fore.YELLOW + Style.BRIGHT + " Phishing Menu ".center(50, '-'))
            print("1. Fake Login Pages")
            print("0. Back to Social Engineering Tools")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Menu de Phishing ".center(50, '-'))
            print("1. Páginas de Logins Falsas")
            print("0. Voltar para Ferramentas de Engenharia Social")

        choice = input("Choose an option: ")

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
        print("Choose a website to clone for fake login:")
        print("1. Facebook")
        print("2. Google")
        print("3. LinkedIn")
        print("0. Back to Phishing Menu")
    else:
        print("Escolha um site para clonar para login falso:")
        print("1. Facebook")
        print("2. Google")
        print("3. LinkedIn")
        print("0. Voltar para o Menu de Phishing")

    choice = input("Enter your choice: ")

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
        print("Credentials captured:")
        print(f"Username/Email: {username}")
        print(f"Password: {password}")
        input("Press Enter to continue...")

    else:
        handle_invalid_option(language)

# Função para informações de número de telefone
def phone_number_info(language):
    clear_console()
    if language == '1':
        print("Phone Number Information")
        print("Enter a phone number to obtain information (country code + operator area code:")
    else:
        print("Informações de Número de Telefone")
        print("Digite um número de telefone para obter informações (código do país + DDD da operadora:")

    phone_number = input("Phone number: ")

    # Realizando a validação do número de telefone usando a API numlookup
    try:
        response = requests.get(f"https://api.numlookupapi.com/v1/validate/{phone_number}?apikey=num_live_nPxUn5CQCi43HYw85qiaohr9FvykkoqCa1x8QkEy")
        data = response.json()

        if data.get("valid"):
            print("Phone number information:")
            print(f"Number: {data.get('number')}")
            print(f"Local format: {data.get('local_format')}")
            print(f"International format: {data.get('international_format')}")
            print(f"Country prefix: {data.get('country_prefix')}")
            print(f"Country code: {data.get('country_code')}")
            print(f"Country name: {data.get('country_name')}")
            print(f"Location: {data.get('location')}")
            print(f"Carrier: {data.get('carrier')}")
            print(f"Line type: {data.get('line_type')}")
        else:
            print("Invalid phone number.")

    except Exception as e:
        print(Fore.RED + f"Error fetching phone number information: {e}")

    input("Press Enter to continue...")

# Função principal para iniciar o programa
def start_program():
    init(autoreset=True)
    language = input("Choose language (1. English / 2. Portuguese): ")

    if language not in ['1', '2']:
        print("Invalid choice. Defaulting to English.")
        language = '1'

    welcome_message(language)
    main_menu(language)

# Início do programa
if __name__ == "__main__":
    start_program()
