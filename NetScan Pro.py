import time
import os
import socket
import ipaddress
import requests
from colorama import init, Fore, Style
from datetime import datetime
import git

def clear_console():
    """Limpa o console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_screen():
    print("Loading...")
    time.sleep(1)
    clear_console()
    print(Style.BRIGHT + "@wbrunnno".center(100))
    time.sleep(2)
    clear_console()

def enter_network(language):
    if language == '1':
        network = input("Enter the network to scan (e.g., 192.168.1.0/24): ")
    else:
        network = input("Digite a rede para escanear (por exemplo, 192.168.1.0/24): ")
    return network

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to retrieve public IP.")
            return None
    except Exception as e:
        print("An error occurred while retrieving public IP:", e)
        return None

def is_port_open(host, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False

def scan_host(host, ports, timeout):
    open_ports = []
    for port in ports:
        if is_port_open(host, port, timeout):
            open_ports.append(port)
    return open_ports

def scan_network(network, ports, timeout):
    network = ipaddress.ip_network(network, strict=False)
    active_hosts = []

    for ip in network.hosts():
        open_ports = scan_host(str(ip), ports, timeout)
        if open_ports:
            active_hosts.append((str(ip), open_ports))
        print(".", end="", flush=True)
    print()

    return active_hosts

def save_scan_results(network, results):
    if os.name == 'nt':
        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

    if not os.path.exists(desktop):
        os.makedirs(desktop)

    filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(desktop, filename)
    
    with open(filepath, 'w') as file:
        file.write(f"Results for network {network}:\n")
        for host, open_ports in results:
            file.write(f"Host: {host}\n")
            for port in open_ports:
                file.write(f"  Port {port} is open\n")
    
    return filepath

def manual_mode(network, language):
    if language == '1':
        ports_input = input("Enter the ports to scan (comma-separated, e.g., 22,80,443): ")
        print(f"Scanning ports: {ports_input}")
    else:
        ports_input = input("Digite as portas para escanear (separadas por vírgula, ex.: 22,80,443): ")
        print(f"Escaneando portas: {ports_input}")

    ports = [int(port.strip()) for port in ports_input.split(',')]

    while True:
        try:
            results = scan_network(network, ports, timeout=1.0)

            if results:
                if language == '1':
                    print(f"Results for network {network}:")
                else:
                    print(f"Resultados para a rede {network}:")
                for host, open_ports in results:
                    print(f"Host: {host}")
                    for port in open_ports:
                        print(f"  Port {port} is open")
            else:
                if language == '1':
                    print("No open ports found.")
                else:
                    print("Nenhuma porta aberta encontrada.")

            filepath = save_scan_results(network, results)
            if language == '1':
                print(f"A report has been generated and saved at {filepath}")
            else:
                print(f"Um relatório foi gerado e salvo em {filepath}")

            time.sleep(10)
            clear_console()

            if language == '1':
                choice = input("Choose an option: (1) Scan another port, (2) Test the same ports again, (3) Back to main menu: ")
            else:
                choice = input("Escolha uma opção: (1) Escanear outra porta, (2) Testar as mesmas portas novamente, (3) Voltar ao menu principal: ")
            
            if choice == '1':
                if language == '1':
                    new_port = int(input("Enter the port to scan: "))
                    print(f"Added port {new_port} to scan.")
                else:
                    new_port = int(input("Digite a porta para escanear: "))
                    print(f"Porta {new_port} adicionada para escanear.")
                ports.append(new_port)
            elif choice == '2':
                continue
            elif choice == '3':
                return
            else:
                if language == '1':
                    print("Invalid option. Please choose again.")
                else:
                    print("Opção inválida. Por favor, escolha novamente.")
        except Exception as e:
            print("An error occurred:", e)

def scan_own_network(language):
    own_ip = socket.gethostbyname(socket.gethostname())
    own_subnet = ".".join(own_ip.split('.')[:3]) + ".0/24"
    if language == '1':
        print(f"Scanning own network {own_subnet}...")
        ports_input = input("Enter the ports to scan (comma-separated, e.g., 22,80,443): ")
        print(f"Scanning ports: {ports_input}")
        ports = [int(port.strip()) for port in ports_input.split(',')]
    else:
        print(f"Escaneando a própria rede {own_subnet}...")
        ports_input = input("Digite as portas para escanear (separadas por vírgula, ex.: 22,80,443): ")
        print(f"Escaneando portas: {ports_input}")
        ports = [int(port.strip()) for port in ports_input.split(',')]
    
    try:
        results = scan_network(own_subnet, ports, timeout=1.0)

        if results:
            if language == '1':
                print(f"Results for own network {own_subnet}:")
            else:
                print(f"Resultados para a própria rede {own_subnet}:")
            for host, open_ports in results:
                print(f"Host: {host}")
                for port in open_ports:
                    print(f"  Port {port} is open")
        else:
            if language == '1':
                print("No open ports found.")
            else:
                print("Nenhuma porta aberta encontrada.")

        filepath = save_scan_results(own_subnet, results)
        if language == '1':
            print(f"A report has been generated and saved at {filepath}")
        else:
            print(f"Um relatório foi gerado e salvo em {filepath}")

        time.sleep(10)
        clear_console()

    except Exception as e:
        print("An error occurred:", e)

def vulnerability_scan_mode(language):
    while True:
        try:
            if language == '1':
                public_ip = get_public_ip()
                if public_ip:
                    print(f"Your public IP address is: {public_ip}")
                    ports_input = input("Enter the ports to scan (comma-separated, e.g., 22,80,443): ")
                    print(f"Scanning ports: {ports_input}")
                    ports = [int(port.strip()) for port in ports_input.split(',')]
                else:
                    print("Unable to retrieve public IP address.")
                    return
            else:
                public_ip = get_public_ip()
                if public_ip:
                    print(f"Seu endereço de IP público é: {public_ip}")
                    ports_input = input("Digite as portas para escanear (separadas por vírgula, ex.: 22,80,443): ")
                    print(f"Escaneando portas: {ports_input}")
                    ports = [int(port.strip()) for port in ports_input.split(',')]
                else:
                    print("Não foi possível recuperar o endereço de IP público.")
                    return

            results = scan_host(public_ip, ports, timeout=1.0)

            if results:
                if language == '1':
                    print(f"Results for public IP {public_ip}:")
                else:
                    print(f"Resultados para o IP público {public_ip}:")
                for port in results:
                    print(f"  Port {port} is open")
            else:
                if language == '1':
                    print("No open ports found.")
                else:
                    print("Nenhuma porta aberta encontrada.")

            time.sleep(10)
            clear_console()

            if language == '1':
                choice = input("Choose an option: (1) Scan again, (2) Back to main menu: ")
            else:
                choice = input("Escolha uma opção: (1) Escanear novamente, (2) Voltar ao menu principal: ")

            if choice == '1':
                continue
            elif choice == '2':
                return
            else:
                if language == '1':
                    print("Invalid option. Please choose again.")
                else:
                    print("Opção inválida. Por favor, escolha novamente.")
        except Exception as e:
            print("An error occurred:", e)

def update_tool(language):
    repo_url = "URL_DO_SEU_REPOSITORIO_GIT"
    local_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        repo = git.Repo(local_dir)
        before = set(repo.head.commit.diff(None))
        repo.remotes.origin.pull()
        after = set(repo.head.commit.diff(None))

        updated_files = after - before
        if updated_files:
            if language == '1':
                print("The following files have been updated:")
            else:
                print("Os seguintes arquivos foram atualizados:")
            for file in updated_files:
                print(f"  {file.a_path} ({file.change_type})")
        else:
            if language == '1':
                print("The tool has been updated successfully.")
            else:
                print("A ferramenta foi atualizada com sucesso.")

        time.sleep(10)
        clear_console()

    except Exception as e:
        print(f"An error occurred while updating the tool: {e}")

def main_menu():
    init(autoreset=True)
    loading_screen()

    while True:
        clear_console()

        print(Fore.CYAN + Style.BRIGHT + " Main Menu ".center(50, "*"))
        print(Fore.CYAN + "1. English")
        print(Fore.CYAN + "2. Português")
        print(Fore.CYAN + "0. Exit")
        print(Fore.CYAN + "*" * 50)

        language = input(Fore.CYAN + "Choose a language / Escolha um idioma: ")

        if language == '0':
            break
        elif language == '1' or language == '2':
            clear_console()

            while True:
                print(Fore.CYAN + Style.BRIGHT + " Network Scanner ".center(50, "*"))
                if language == '1':
                    print(Fore.CYAN + "1. Enter network to scan")
                    print(Fore.CYAN + "2. Scan own network")
                    print(Fore.CYAN + "3. Vulnerability scan mode")
                    print(Fore.CYAN + "4. Update Tool")
                    print(Fore.CYAN + "0. Back to main menu")
                else:
                    print(Fore.CYAN + "1. Digite a rede para escanear")
                    print(Fore.CYAN + "2. Escanear a própria rede")
                    print(Fore.CYAN + "3. Modo de varredura de vulnerabilidades")
                    print(Fore.CYAN + "4. Atualizar Ferramenta")
                    print(Fore.CYAN + "0. Voltar ao menu principal")
                print(Fore.CYAN + "*" * 50)

                option = input(Fore.CYAN + "Choose an option / Escolha uma opção: ")

                if option == '0':
                    break
                elif option == '1':
                    network = enter_network(language)
                    manual_mode(network, language)
                elif option == '2':
                    scan_own_network(language)
                elif option == '3':
                    vulnerability_scan_mode(language)
                elif option == '4':
                    update_tool(language)
                else:
                    if language == '1':
                        print("Invalid option. Please choose again.")
                    else:
                        print("Opção inválida. Por favor, escolha novamente.")
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main_menu()
