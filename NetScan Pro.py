import time
import os
import socket
import ipaddress
import requests
import webbrowser
from colorama import init, Fore, Style
from datetime import datetime

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
        print(f"Scanning ports: {ports}")
    else:
        ports_input = input("Digite as portas para escanear (separadas por vírgula, ex.: 22,80,443): ")
        print(f"Escaneando portas: {ports}")

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
        ports = [int(port.strip()) for port in ports_input.split(',')]
    else:
        print(f"Escaneando a própria rede {own_subnet}...")
        ports_input = input("Digite as portas para escanear (separadas por vírgula, ex.: 22,80,443): ")
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

def instagram():
    webbrowser.open("https://www.instagram.com/wbrunnno/")

def public_ip(language):
    ip = get_public_ip()
    if ip:
        if language == '1':
            print("Your public IP address:", ip)
        else:
            print("Seu endereço IP público:", ip)

if __name__ == "__main__":
    init()
    loading_screen()
    language = input("Choose language / Escolha o idioma: (1) English (2) Português: ")

    while True:
        if language == '1':
            print("Main Menu:")
            print("1. Enter the network to scan (e.g., 192.168.1.0/24)")
            print("2. Scan your own network")
            print("3. Check your public IP")
            print("4. Visit my Instagram @wbrunnno")
            print("5. Exit")
        else:
            print("Menu Principal:")
            print("1. Digite a rede para escanear (por exemplo, 192.168.1.0/24)")
            print("2. Escanear sua própria rede")
            print("3. Verificar seu IP público")
            print("4. Visite meu Instagram @wbrunnno")
            print("5. Sair")

        choice = input("Enter your choice / Digite sua escolha: ")

        if choice == '1':
            network = enter_network(language)
            if language == '1':
                mode = input("Choose mode: (1) Automatic ports (2) Manual ports: ")
            else:
                mode = input("Escolha o modo: (1) Portas automáticas (2) Portas manuais: ")

            if mode == '1':
                ports = list(range(1, 1025))
                if language == '1':
                    print(f"Scanning network {network} with ports {ports}...")
                else:
                    print(f"Escaneando a rede {network} com portas {ports}...")

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

                except Exception as e:
                    print("An error occurred:", e)
            elif mode == '2':
                manual_mode(network, language)
            else:
                if language == '1':
                    print("Invalid mode selected. Exiting.")
                else:
                    print("Modo inválido selecionado. Saindo.")
                break
        elif choice == '2':
            scan_own_network(language)
        elif choice == '3':
            public_ip(language)
        elif choice == '4':
            instagram()
        elif choice == '5':
            if language == '1':
                print("Exiting the program. Goodbye!")
            else:
                print("Saindo do programa. Até logo!")
            break
        else:
            if language == '1':
                print("Invalid choice. Please enter a number from 1 to 5.")
            else:
                print("Escolha inválida. Por favor, digite um número de 1 a 5.")
