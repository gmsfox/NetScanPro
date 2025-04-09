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
import sys
import numlookupapi
from colorama import init, Fore, Style

# Função para limpar a tela do console
def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    # Função para atualizar dependências do projeto
def update_dependencies_crossplatform():
    """
    Atualiza as dependências do projeto e gera automaticamente o arquivo requirements.txt.
    Funciona em qualquer sistema operacional.
    """
    clear_console()
    print(Fore.YELLOW + Style.BRIGHT + "Atualizando dependências do projeto...")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "numlookupapi"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pipreqs"])
        subprocess.check_call([sys.executable, "-m", "pipreqs", ".", "--force", "--encoding=utf-8"])
        print(Fore.GREEN + "[✔] requirements.txt atualizado com sucesso!")
    except Exception as e:
        print(Fore.RED + f"[!] Erro ao atualizar dependências: {e}")

    input("\\nPressione Enter para continuar...")

# Função para exibir a mensagem de boas-vindas
def welcome_message(user_language):
    """
    Exibe uma mensagem de boas-vindas com base no idioma selecionado pelo usuário.

    Parameters:
    user_language (str): O idioma escolhido pelo usuário. Deve ser '1' para inglês 
    ou '2' para português.

    Returns:
    None
    """
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
    """
    Exibe uma mensagem de agradecimento ao usuário com base no idioma selecionado.

    Parameters:
    user_language (str): O idioma escolhido pelo usuário. Deve ser '1' para inglês 
    ou '2' para português.

    Returns:
    None
    """
    clear_console()
    if user_language == '1':
        print(Fore.GREEN + Style.BRIGHT + "Thank you for using NetScan Pro tool!".center(50))
    else:
        print(Fore.GREEN + Style.BRIGHT + "Obrigado por usar a ferramenta NetScan Pro!".center(50))
    time.sleep(3)
    print()

# Função para lidar com opções inválidas
def handle_invalid_option(user_language):
    """
    Exibe uma mensagem de erro para uma opção inválida com base no idioma selecionado.

    Parameters:
    user_language (str): O idioma escolhido pelo usuário. Deve ser '1' para inglês
                         ou '2' para português.

    Returns:
    None
    """
    clear_console()
    if user_language == '1':
        print(Fore.RED + "Invalid option. Please choose again.")
    else:
        print(Fore.RED + "Opção inválida. Por favor, escolha novamente.")
    time.sleep(2)

# Função para exibir a mensagem de carregamento
def loading_screen():
    """
    Exibe uma tela de carregamento temporária com uma mensagem.

    A função imprime "Loading...", aguarda 3 segundos, limpa o console, exibe 
    uma mensagem centralizada com estilo brilhante e aguarda mais 1 segundo 
    antes de continuar.

    Returns:
    None
    """
    print("Loading...")
    time.sleep(3)
    clear_console()
    print(Style.BRIGHT + "@wbrunnno".center(60))
    time.sleep(1)

# Função para atualizar a ferramenta do GitHub
def update_tool_from_github(user_language):
    """
    Atualiza a ferramenta NetScan Pro a partir do repositório GitHub e reinicia a ferramenta.

    Esta função executa um comando Git para atualizar o repositório da ferramenta, 
    exibe mensagens de status de atualização e reinicia a ferramenta após a atualização.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).

    Retorna:
    None
    """
    clear_console()
    print(Fore.YELLOW + Style.BRIGHT + "Updating NetScan Pro tool from GitHub...")

    try:
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
    """
    Exibe o menu principal da ferramenta e gerencia a navegação para outras opções.

    Este menu oferece opções para acessar ferramentas de rede, ferramentas de engenharia social, 
    atualizar a ferramenta e sair. Dependendo da escolha do usuário, a função direciona o fluxo 
    para a função correspondente ou lida com opções inválidas.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).

    Retorna:
    None
    """
    while True:
        clear_console()
        if user_language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Main Menu ".center(50, '-'))
            print("1. Network Tools")
            print("2. Social Engineering Tools")
            print("3. Update Tool")
            print("4. Update Project Dependencies")
            print("0. Exit")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Menu Principal ".center(50, '-'))
            print("1. Ferramentas de Rede")
            print("2. Ferramentas de Engenharia Social")
            print("3. Atualizar Ferramenta")
            print("4. Atualizar Dependências do Projeto")
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
        elif choice == '4':
            update_dependencies_crossplatform()
        else:
            handle_invalid_option(user_language)

# Função para o menu de ferramentas de rede
def network_tools_menu(user_language):
    """
    Exibe o menu de ferramentas de rede e gerencia a navegação para as opções disponíveis.

    Este menu oferece opções para escanear uma rede, escanear a própria rede, realizar um 
    escaneamento de vulnerabilidades e retornar ao menu principal. Dependendo da escolha do 
    usuário, a função direciona o fluxo para a função correspondente ou lida com opções inválidas.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).

    Retorna:
    None
    """
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
    """
    Solicita ao usuário o nome da rede para escanear e retorna o valor inserido.

    Dependendo do idioma escolhido pelo usuário, a função exibe uma mensagem em inglês ou 
    português solicitando o nome da rede.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).

    Retorna:
    str: O nome da rede inserido pelo usuário.
    """
    clear_console()
    if user_language == '1':
        return input("Enter the network name: ")
    else:
        return input("Digite o nome da rede: ")

# Função para o modo manual
def manual_mode(user_language):
    """
    Exibe uma mensagem indicando que o escaneamento de rede está sendo realizado no modo manual.

    Dependendo do idioma escolhido pelo usuário, a função exibe uma mensagem em inglês ou 
    português indicando que o escaneamento está em andamento no modo manual.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).
    """
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
    """
    Exibe uma mensagem indicando que o escaneamento da própria rede está sendo realizado.

    Dependendo do idioma escolhido pelo usuário, a função exibe uma mensagem em inglês ou 
    português indicando que o escaneamento da própria rede está em andamento.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).
    """
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
    """
    Exibe uma mensagem indicando que o escaneamento de vulnerabilidades está sendo realizado.

    Dependendo do idioma escolhido pelo usuário, a função exibe uma mensagem em inglês ou 
    português indicando que o escaneamento de vulnerabilidades está em andamento.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).
    """
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
    """
    Exibe o menu de ferramentas de engenharia social e lida com a seleção de opções.

    Dependendo do idioma escolhido pelo usuário, a função exibe um menu com opções relacionadas
    a ferramentas de engenharia social. Permite que o usuário escolha entre obter informações de
    um número de telefone ou acessar a opção de phishing. Também oferece a opção de retornar ao
    menu principal.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).
    """
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
    """
    Exibe o menu de phishing e lida com a seleção de opções.

    Dependendo do idioma escolhido pelo usuário, a função exibe um menu com opções relacionadas
    a phishing. Permite que o usuário escolha entre criar páginas de login falsas ou retornar
    para as ferramentas de engenharia social. Também oferece a opção de retornar ao menu anterior.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).
    """
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
    """
    Cria uma página de login falsa e inicia um servidor HTTP para servir a página.

    Dependendo do idioma escolhido pelo usuário, a função solicita a URL do site a ser clonado
    e cria uma página de login falsa. A página é salva localmente e um servidor HTTP é iniciado
para servir essa página. O servidor continua a ser executado até que seja interrompido manualmente.

    Parâmetros:
    user_language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).
    """
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

def save_phone_number_info(phone_number, result, language):
    """
    Salva as informações do número de telefone em um arquivo de texto.

   O nome do arquivo é baseado no número de telefone fornecido. As informações são salvas no arquivo
    em inglês ou português, dependendo do idioma selecionado.

    Parâmetros:
    phone_number (str): O número de telefone para o qual as informações serão salvas.
    result (dict): Um dicionário contendo as informações detalhadas sobre o número de telefone.
    language (str): O idioma escolhido pelo usuário ('1' para inglês, '2' para português).
    """
    # Define o nome do arquivo com base no número de telefone
    filename = f"{phone_number}_info.txt"

    with open(filename, 'w') as file:
        if language == '1':
            # Escreve as informações em inglês
            file.write(f"Information for phone number {phone_number}\n")
            file.write(f"Valid: {result.get('valid', False)}\n")
            file.write(f"Number: {result.get('number', '')}\n")
            file.write(f"Local Format: {result.get('local_format', '')}\n")
            file.write(f"International Format: {result.get('international_format', '')}\n")
            file.write(f"Country Prefix: {result.get('country_prefix', '')}\n")
            file.write(f"Country Code: {result.get('country_code', '')}\n")
            file.write(f"Country Name: {result.get('country_name', '')}\n")
            file.write(f"Location: {result.get('location', '')}\n")
            file.write(f"Carrier: {result.get('carrier', '')}\n")
            file.write(f"Line Type: {result.get('line_type', '')}\n")
        else:
            # Escreve as informações em português
            file.write(f"Informações para o número de telefone {phone_number}\n")
            file.write(f"Válido: {result.get('valid', False)}\n")
            file.write(f"Número: {result.get('number', '')}\n")
            file.write(f"Formato Local: {result.get('local_format', '')}\n")
            file.write(f"Formato Internacional: {result.get('international_format', '')}\n")
            file.write(f"Prefixo do País: {result.get('country_prefix', '')}\n")
            file.write(f"Código do País: {result.get('country_code', '')}\n")
            file.write(f"Nome do País: {result.get('country_name', '')}\n")
            file.write(f"Localização: {result.get('location', '')}\n")
            file.write(f"Operadora: {result.get('carrier', '')}\n")
            file.write(f"Tipo de Linha: {result.get('line_type', '')}\n")
    if language == '1':
        print("Information saved to", filename)
    else:
        print("Informações salvas em", filename)

# Função para obter informações sobre números de telefone
def phone_number_info(user_language):
    """
    Obtém informações detalhadas sobre um número de telefone e exibe os dados.

    Dependendo do idioma selecionado pelo usuário, a função exibe as informações
    sobre o número de telefone em inglês ou português. As informações são obtidas
    através da API numlookupapi e, em seguida, salvas em um arquivo de texto.

    Parâmetros:
    user_language (str): O idioma selecionado pelo usuário ('1' para inglês, '2' para português).
    """
    clear_console()
    if user_language == '1':
        print("Enter the phone number to get information:")
    else:
        print("Digite o número de telefone para obter informações:")

    phone_number = input(
    "Phone number: " if user_language == '1'
    else "Número de telefone: "
)   # Consulta à API numlookupapi para obter informações detalhadas
    try:
        client = numlookupapi.Client(
    'num_live_nPxUn5CQCi43HYw85qiaohr9FvykkoqCa1x8QkEy'  # Substitua 'YOUR-API-KEY' pelo seu API key
    )
        result = client.validate(phone_number) # Ajuste a função de acordo com a documentação

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

             # Salva as informações em um arquivo de texto
            save_phone_number_info(phone_number, result, user_language)

    except Exception as e:
        print(Fore.RED + f"Error fetching phone number information: {e}")

    input(
    "\nPress Enter to continue..." if user_language == '1'
    else "\nPressione Enter para continuar..."
)
# Função principal para iniciar o programa
def main():
    """
    Função principal que inicializa a aplicação, permite ao usuário selecionar o idioma,
    exibe a mensagem de boas-vindas e exibe o menu principal.

    O processo inclui:
    1. Inicialização do terminal com configurações de cores.
    2. Limpeza do console e exibição da seleção de idioma.
    3. Captura da escolha do idioma do usuário.
    4. Definição do idioma padrão se a escolha for inválida.
    5. Exibição da mensagem de boas-vindas.
    6. Exibição do menu principal com base na escolha do idioma.
    """
    init(autoreset=True)

    # Selecionar o idioma
    clear_console()
    print(Fore.YELLOW + Style.BRIGHT + " Language Selection ".center(50, '-'))
    print("1. English")
    print("2. Português")

    language_option = input("Choose your language: ")

    if language_option == '1' or language_option == '2':
        user_language = language_option
    else:
        user_language = '1'  # Default to English

    welcome_message(user_language)
    main_menu(user_language)

if __name__ == "__main__":
    main()
