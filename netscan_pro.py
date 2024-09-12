"""
NetScan Pro

Ferramenta para escaneamento de redes e execução de técnicas de engenharia social.
Inclui funcionalidades de consulta a números e clonagem de sites.

Autor: Wevertton Bruno
Data: 2024
"""


import os
import subprocess
import http.server
import socketserver
import threading
import time
import urllib.parse
import json
import numlookupapi
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

# Função para limpar a tela do console
def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para exibir a mensagem de boas-vindas
def welcome_message(user_language):
    clear_console()
    if user_language == '1':
        print(Fore.GREEN + Style.BRIGHT + "Welcome to the NetScan Pro tool!".center(50))
    else:
        print(Fore.GREEN + Style.BRIGHT + "Bem-vindo à ferramenta NetScan Pro!".center(50))
    print()
    time.sleep(2)
    clear_console()

# Função para exibir a mensagem de despedida
def goodbye_message(user_language):
    clear_console()
    if user_language == '1':
        print(Fore.GREEN + Style.BRIGHT + "Thank you for using NetScan Pro tool!".center(50))
    else:
        print(Fore.GREEN + Style.BRIGHT + "Obrigado por usar a ferramenta NetScan Pro!".center(50))
    time.sleep(3)
    print()

# Função para lidar com opções inválidas
def handle_invalid_option(user_language):
    clear_console()
    if user_language == '1':
        print(Fore.RED + "Invalid option. Please choose again.")
    else:
        print(Fore.RED + "Opção inválida. Por favor, escolha novamente.")
    time.sleep(2)

# Função para exibir a mensagem de carregamento
def loading_screen():
    print("Loading...")
    time.sleep(3)
    clear_console()
    print(Style.BRIGHT + "@wbrunnno".center(60))
    time.sleep(1)

# Função para atualizar a ferramenta do GitHub
def update_tool_from_github(user_language):
    clear_console()
    print(Fore.YELLOW + Style.BRIGHT + "Updating NetScan Pro tool from GitHub...")

    try:
        # Atualização usando Git
        subprocess.run(["git", "pull", "https://github.com/WeverttonBruno/NetScanPro.git"], 
        check=True)
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
    main_menu(user_language)

# Função para exibir o menu principal
def main_menu(user_language):
    while True:
        clear_console()
        if user_language == '1':
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
            goodbye_message(user_language)
            break
        elif choice == '1':
            network_tools_menu(user_language)
        elif choice == '2':
            social_engineering_tools(user_language)
        elif choice == '3':
            update_tool_from_github(user_language)
        else:
            handle_invalid_option(user_language)

# Função para o menu de ferramentas de rede
def network_tools_menu(user_language):
    while True:
        clear_console()
        if user_language == '1':
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
            enter_network(user_language)
            manual_mode(user_language)
        elif choice == '2':
            scan_own_network(user_language)
        elif choice == '3':
            vulnerability_scan_mode(user_language)
        else:
            handle_invalid_option(user_language)

# Função para entrar com o nome da rede
def enter_network(user_language):
    clear_console()
    if user_language == '1':
        return input("Enter the network name: ")
    else:
        return input("Digite o nome da rede: ")

# Função para o modo manual
def manual_mode(user_language):
    clear_console()
    if user_language == '1':
        print("Scanning network in manual mode...")
    else:
        print("Escanenado rede no modo manual...")

    # Lógica para o modo manual (simulado)
    time.sleep(3)
    input("Press Enter to continue...")

# Função para escanear a própria rede
def scan_own_network(user_language):
    clear_console()
    if user_language == '1':
        print("Scanning own network...")
    else:
        print("Escanenando a própria rede...")

    # Lógica para escanear a própria rede (simulado)
    time.sleep(3)
    input("Press Enter to continue...")

# Função para o escaneamento de vulnerabilidades
def vulnerability_scan_mode(user_language):
    clear_console()
    if user_language == '1':
        print("Vulnerability scanning...")
    else:
        print("Escaneamento de vulnerabilidades...")

    # Lógica para o escaneamento de vulnerabilidades (simulado)
    time.sleep(3)
    input("Press Enter to continue...")

# Função para o menu de ferramentas de engenharia social
def social_engineering_tools(user_language):
    while True:
        clear_console()
        if user_language == '1':
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
            phone_number_info(user_language)
        elif choice == '2':
            phishing_menu(user_language)
        else:
            handle_invalid_option(user_language)

# Função para o submenu de phishing
def phishing_menu(user_language):
    while True:
        clear_console()
        if user_language == '1':
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
            fake_login_pages(user_language)
        else:
            handle_invalid_option(user_language)

# Função para as páginas de logins falsas
def fake_login_pages(user_language):
    clear_console()
    if user_language == '1':
        print("Enter the URL of the website to clone for fake login:")
    else:
        print("Digite a URL do site para clonar para login falso:")

    url = input("URL: ")

    # Selecionar o servidor (apenas localhost implementado)
    server = 'localhost'
    port = 8080

    # Função para criar a página falsa
    def create_fake_login_page():
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login</title>
        </head>
        <body>
            <h1>Login</h1>
            <form action="/submit" method="post">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username"><br>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """
        return html_content

    # Função para criar o servidor HTTP
    def start_http_server():
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer((server, port), handler)
        print(f"Serving at http://{server}:{port}")
        httpd.serve_forever()

    # Criar a página falsa
    fake_login_html = create_fake_login_page()

    # Salvar a página falsa
    with open('fake_login.html', 'w') as file:
        file.write(fake_login_html)

    print("Fake login page created successfully!")

    # Iniciar o servidor HTTP em uma thread separada
    threading.Thread(target=start_http_server, daemon=True).start()

    # Manter o servidor rodando
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down the server...")
        os.remove('fake_login.html')

# Função para obter informações sobre números de telefone
def phone_number_info(user_language):
    clear_console()
    if user_language == '1':
        print("Enter the phone number to get information:")
    else:
        print("Digite o número de telefone para obter informações:")

    phone_number = input("Phone number: " if user_language == '1' else "Número de telefone: ")
    
    # Consulta à API numlookupapi para obter informações detalhadas
    try:
        Client = numlookupapi.Client('num_live_nPxUn5CQCi43HYw85qiaohr9FvykkoqCa1x8QkEy')  # Substitua 'YOUR-API-KEY' pelo seu API key
        result = Client.validate(phone_number) # Ajuste a função de acordo com a documentação
        
        # Formatando a resposta no estilo desejado
        if user_language == '1':
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
        else:
            print("\nInformações para o número de telefone", phone_number)
            print("Válido:", result.get("valid", False))
            print("Número:", result.get("number", ""))
            print("Formato Local:", result.get("local_format", ""))
            print("Formato Internacional:", result.get("international_format", ""))
            print("Prefixo do País:", result.get("country_prefix", ""))
            print("Código do País:", result.get("country_code", ""))
            print("Nome do País:", result.get("country_name", ""))
            print("Localização:", result.get("location", ""))
            print("Operadora:", result.get("carrier", ""))
            print("Tipo de Linha:", result.get("line_type", ""))
            
    except Exception as e:
        print(Fore.RED + f"Error fetching phone number information: {e}")

    input("\nPress Enter to continue..." if user_language == '1' else "\nPressione Enter para continuar...")
# Função principal para iniciar o programa
def main():
    init(autoreset=True)

    # Selecionar o idioma
    clear_console()
    print(Fore.YELLOW + Style.BRIGHT + " Language Selection ".center(50, '-'))
    print("1. English")
    print("2. Portuguese")

    language_option = input("Choose your language: ")

    if language_option == '1' or language_option == '2':
        user_language = language_option
    else:
        user_language = '1'  # Default to English

    welcome_message(user_language)
    main_menu(user_language)

if __name__ == "__main__":
    main()