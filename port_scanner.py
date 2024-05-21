import time
import os
import socket
import ipaddress
import requests
from colorama import init, Fore, Style

def clear_console():
    """Limpa o console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_screen():
    print("Loading...")
    time.sleep(1)  # Aguarda 1 segundo
    clear_console()
    print(Style.BRIGHT + "@wbrunnno".center(100))  # Centraliza o @wbrunnno em uma linha de 100 caracteres com estilo de fonte brilhante
    time.sleep(2)  # Aguarda mais 2 segundos antes de prosseguir
    clear_console()

def enter_network():
    network = input("Enter the network to scan (e.g., 192.168.1.0/24): ")
    return network

def get_public_ip():
    """Obtém o endereço IP público do dispositivo."""
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
    """Verifica se uma porta está aberta em um host dado."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False

def scan_host(host, ports, timeout):
    """Varre um host em busca de portas abertas na lista fornecida."""
    open_ports = []
    for port in ports:
        if is_port_open(host, port, timeout):
            open_ports.append(port)
    return open_ports

def scan_network(network, ports, timeout):
    """Varre uma rede inteira em busca de hosts ativos e portas abertas."""
    network = ipaddress.ip_network(network, strict=False)
    active_hosts = []

    for ip in network.hosts():
        open_ports = scan_host(str(ip), ports, timeout)
        if open_ports:
            active_hosts.append((str(ip), open_ports))
        print(".", end="", flush=True)  # Exibe um ponto para indicar progresso
    print()  # Adiciona uma quebra de linha após a varredura

    return active_hosts

def manual_mode(network):
    ports_input = input("Enter the ports to scan (comma-separated, e.g., 22,80,443): ")
    ports = [int(port.strip()) for port in ports_input.split(',')]
    print(f"Scanning ports: {ports}")

    while True:
        try:
            results = scan_network(network, ports, timeout=1.0)

            if results:
                for host, open_ports in results:
                    print(f"Host: {host}")
                    for port in open_ports:
                        print(f"  Port {port} is open")
            else:
                print("No open ports found.")

            choice = input("Choose an option: (1) Scan another port, (2) Test the same ports again, (3) Back to main menu: ")
            if choice == '1':
                new_port = int(input("Enter the port to scan: "))
                ports.append(new_port)
                print(f"Added port {new_port} to scan.")
            elif choice == '2':
                # Re-scan the same ports
                continue
            elif choice == '3':
                return  # Exit manual mode and return to main menu
            else:
                print("Invalid option. Please choose again.")
        except Exception as e:
            print("An error occurred:", e)

def scan_own_network():
    own_ip = socket.gethostbyname(socket.gethostname())
    own_subnet = ".".join(own_ip.split('.')[:3]) + ".0/24"
    print(f"Scanning own network {own_subnet}...")
    ports_input = input("Enter the ports to scan (comma-separated, e.g., 22,80,443): ")
    ports = [int(port.strip()) for port in ports_input.split(',')]
    try:
        # Varredura da rede local com exibição de progresso
        results = scan_network(own_subnet, ports, timeout=1.0)

        if results:
            for host, open_ports in results:
                print(f"Host: {host}")
                for port in open_ports:
                    print(f"  Port {port} is open")
        else:
            print("No open ports found.")
    except Exception as e:
        print("An error occurred:", e)

def instagram():
    print("Acesse o Instagram @wbrunnno para mais informações.")

def public_ip():
    ip = get_public_ip()
    if ip:
        print("Your public IP address:", ip)

if __name__ == "__main__":
    init()  # Inicializa o colorama
    loading_screen()
    while True:
        print("Menu principal:")
        print("1. Enter the network to scan (e.g., 192.168.1.0/24)")
        print("2. Scan your own network")
        print("3. Check your public IP")
        print("4. Visit my Instagram @wbrunnno")
        choice = input("Enter your choice: ")

        if choice == '1':
            network = enter_network()
            mode = input("Choose mode: (1) Automatic ports (2) Manual ports: ")

            if mode == '1':
                # Define automatic ports to scan (common ports)
                ports = list(range(1, 1025))  # Scanning ports 1-1024
                print(f"Scanning network {network} with ports {ports}...")
                try:
                    # Varredura da rede com exibição de progresso
                    results = scan_network(network, ports, timeout=1.0)

                    if results:
                        for host, open_ports in results:
                            print(f"Host: {host}")
                            for port in open_ports:
                                print(f"  Port {port} is open")
                    else:
                        print("No open ports found.")
                except Exception as e:
                    print("An error occurred:", e)
            elif mode == '2':
                manual_mode(network)
            else:
                print("Invalid mode selected. Exiting.")
                break
        elif choice == '2':
            scan_own_network()
        elif choice == '3':
            public_ip()
        elif choice == '4':
            instagram()
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
