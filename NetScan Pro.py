import os
import subprocess
import requests
import time
import threading
import http.server
import socketserver
import webbrowser
from colorama import init, Fore, Style
from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat
import phonenumbers.geocoder as geocoder
import phonenumbers.carrier as carrier

# Porta para o servidor HTTP local
PORT = 8000

# Diretório onde os arquivos HTML e CSS serão armazenados
HTML_CSS_DIR = 'html_css'
if not os.path.exists(HTML_CSS_DIR):
    os.makedirs(HTML_CSS_DIR)

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
            clone_login_page(language)
        else:
            handle_invalid_option(language)

def clone_login_page(language):
    clear_console()
    if language == '1':
        url = input("Enter the URL of the page to clone: ")
        print("Choose server:\n1. Localhost\n2. Ngrok\n3. Cloudflare")
    else:
        url = input("Digite a URL da página para clonar: ")
        print("Escolha o servidor:\n1. Localhost\n2. Ngrok\n3. Cloudflare")

    server_choice = input("Choose server: ")

    # Diretório onde os arquivos HTML e CSS serão salvos
    base_filename = os.path.basename(url)
    html_path = os.path.join(HTML_CSS_DIR, f"{base_filename}.html")
    css_path = os.path.join(HTML_CSS_DIR, f"{base_filename}.css")

    try:
        # Verificar se o arquivo HTML já existe
        if not os.path.exists(html_path):
            # Baixar o HTML da página
            response = requests.get(url)
            if response.status_code == 200:
                with open(html_path, 'w') as file:
                    file.write(response.text)
                print("HTML downloaded successfully.")

                # Lógica para extrair e baixar o CSS, se necessário
                # Aqui você pode adicionar a lógica para extrair e baixar o CSS
                # Exemplo simples:
                css_content = "/* Adicione seu conteúdo CSS aqui */"
                with open(css_path, 'w') as file:
                    file.write(css_content)
                print("CSS downloaded successfully.")
            else:
                print(Fore.RED + "Failed to download the page.")
                return
        else:
            print(f"{Fore.GREEN}Arquivo HTML para {url} já existe, pulando o download.")

    except Exception as e:
        print(Fore.RED + f"Erro: {e}")
        return

    # Escolher o servidor para usar
    if server_choice == '1':
        start_local_server(language, html_path)
    elif server_choice == '2':
        start_ngrok_server(language, html_path)
    elif server_choice == '3':
        start_cloudflare_server(language, html_path)

def start_local_server(language, html_path):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = html_path
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    clear_console()
    print("Starting local server...")

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Local server running on port {PORT}")
            target_url = f"http://localhost:{PORT}/{os.path.basename(html_path)}"
            print("Opening fake login page in browser...")
            time.sleep(2)
            webbrowser.open(target_url)
            input("\nPress Enter to stop the server...")
            httpd.shutdown()
    except Exception as e:
        print(Fore.RED + f"Error starting server: {e}")

def start_ngrok_server(language, html_path):
    clear_console()
    print("Starting ngrok server...")

    try:
        ngrok_process = subprocess.Popen(["ngrok", "http", str(PORT)], stdout=subprocess.PIPE)
        time.sleep(5)  # Esperar ngrok iniciar
        ngrok_url = "http://localhost:4040/api/tunnels"
        tunnels_response = requests.get(ngrok_url).json()
        public_url = tunnels_response['tunnels'][0]['public_url']
        print(f"Ngrok URL: {public_url}")
        print("Opening fake login page in browser...")
        webbrowser.open(public_url)
        input("\nPress Enter to stop the server...")
        ngrok_process.terminate()
    except Exception as e:
        print(Fore.RED + f"Error starting ngrok server: {e}")

def start_cloudflare_server(language, html_path):
    clear_console()
    print("Starting cloudflare server...")

    try:
        cloudflare_process = subprocess.Popen(["cloudflared", "tunnel", "http", str(PORT)], stdout=subprocess.PIPE)
        time.sleep(5)  # Esperar Cloudflare iniciar
        cloudflare_url = "http://localhost:4040/api/tunnels"
        tunnels_response = requests.get(cloudflare_url).json()
        public_url = tunnels_response['tunnels'][0]['public_url']
        print(f"Cloudflare URL: {public_url}")
        print("Opening fake login page in browser...")
        webbrowser.open(public_url)
        input("\nPress Enter to stop the server...")
        cloudflare_process.terminate()
    except Exception as e:
        print(Fore.RED + f"Error starting cloudflare server: {e}")

# Função para obter informações de número de telefone
def phone_number_info(language):
    clear_console()
    if language == '1':
        phone_number = input("Enter the phone number (e.g., +1234567890): ")
    else:
        phone_number = input("Digite o número de telefone (e.g., +1234567890): ")

    try:
        number = parse(phone_number)
        if is_valid_number(number):
            info = {
                "valid": True,
                "number": phone_number,
                "local_format": format_number(number, PhoneNumberFormat.NATIONAL),
                "international_format": format_number(number, PhoneNumberFormat.INTERNATIONAL),
                "country_prefix": number.country_code,
                "country_code": number.country_code,
                "country_name": geocoder.country_name_for_number(number, "en"),
                "location": geocoder.description_for_number(number, "en"),
                "carrier": carrier.name_for_number(number, "en"),
            }
            clear_console()
            print("Phone Number Information".center(50, '-'))
            for key, value in info.items():
                print(f"{key}: {value}")
        else:
            print(Fore.RED + "No information found for this phone number.")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

    input("\nPress Enter to return to the Social Engineering Tools menu...")

# Função principal para iniciar o programa
def start_program():
    clear_console()
    print("1. English\n2. Português")
    language = input("Choose a language / Escolha um idioma: ")

    if language not in ['1', '2']:
        handle_invalid_option('1')
        return

    welcome_message(language)
    loading_screen()
    main_menu(language)

if __name__ == "__main__":
    start_program()
