import subprocess
import os
from typing import Tuple
import logging
from pathlib import Path

class VPNManager:
    @staticmethod
    def _run_command(cmd: list) -> Tuple[bool, str]:
        """Executa comandos com tratamento robusto de erros"""
        try:
            result = subprocess.run(cmd,
                                  check=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=120)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() or f"Command failed with code {e.returncode}"
            return False, error_msg
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _install_deb_package() -> Tuple[bool, str]:
        """Instala o pacote .deb e configura repositórios"""
        try:
            # Verifica se o arquivo .deb existe
            deb_file = "protonvpn-stable-release_1.0.8_all.deb"
            if not os.path.exists(deb_file):
                return False, f"Arquivo {deb_file} não encontrado"

            # 1. Instala o pacote .deb
            success, error = VPNManager._run_command(
                ["sudo", "dpkg", "-i", deb_file])
            if not success:
                return False, f"Falha ao instalar .deb: {error}"

            # 2. Atualiza os repositórios
            success, error = VPNManager._run_command(
                ["sudo", "apt", "update", "-y"])
            if not success:
                return False, f"Falha ao atualizar repositórios: {error}"

            return True, "Pacote .deb e repositórios configurados"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _install_vpn_client() -> Tuple[bool, str, str]:
        """Tenta instalar o cliente VPN (GUI ou CLI)"""
        clients = ["proton-vpn-gnome-desktop", "protonvpn-cli"]
        for client in clients:
            success, error = VPNManager._run_command(
                ["sudo", "apt", "install", "-y", client])
            if success:
                return True, client, f"Cliente {client} instalado"
        return False, "", "Falha ao instalar ambos clientes GUI e CLI"

    @staticmethod
    def check_installation() -> bool:
        """Verifica se qualquer versão está instalada"""
        checks = [
            ["which", "protonvpn-cli"],
            ["which", "proton-vpn-gnome-desktop"],
            ["dpkg", "-l", "proton-vpn-gnome-desktop"]
        ]
        return any(VPNManager._run_command(cmd)[0] for cmd in checks)

    @staticmethod
    def install() -> Tuple[bool, str]:
        """Fluxo completo de instalação"""
        try:
            # 1. Instala pacote .deb e configura repositórios
            print("Configurando repositórios ProtonVPN...")
            success, message = VPNManager._install_deb_package()
            if not success:
                return False, message

            # 2. Instala o cliente VPN
            print("Instalando cliente VPN...")
            success, client_type, message = VPNManager._install_vpn_client()
            if not success:
                return False, message

            return True, f"Instalação concluída ({client_type})"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Configura login para o cliente instalado"""
        try:
            # Detecta qual cliente está instalado
            clients = {
                "protonvpn-cli": ["sudo", "protonvpn-cli", "login", "--username", username, "--password", password],
                "proton-vpn-gnome-desktop": ["protonvpn-cli", "login", username, password]
            }

            for client, cmd in clients.items():
                success, _ = VPNManager._run_command(["which", client.split()[0]])
                if success:
                    return VPNManager._run_command(cmd)

            return False, "Nenhum cliente ProtonVPN encontrado"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def connect() -> Tuple[bool, str]:
        """Conecta usando o cliente disponível"""
        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for client in clients:
            success, _ = VPNManager._run_command(["which", client])
            if success:
                return VPNManager._run_command([client, "connect", "--fastest"])
        return False, "Nenhum cliente ProtonVPN instalado"

    @staticmethod
    def disconnect() -> Tuple[bool, str]:
        """Desconecta usando o cliente disponível"""
        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for client in clients:
            success, _ = VPNManager._run_command(["which", client])
            if success:
                return VPNManager._run_command([client, "disconnect"])
        return False, "Nenhum cliente ProtonVPN instalado"

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verifica status usando o cliente disponível"""
        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for client in clients:
            success, _ = VPNManager._run_command(["which", client])
            if success:
                return VPNManager._run_command([client, "status"])
        return False, "Nenhum cliente ProtonVPN instalado"

    @staticmethod
    def cleanup() -> Tuple[bool, str]:
        """Remove completamente a instalação"""
        try:
            commands = [
                ["sudo", "apt", "remove", "--purge", "-y", "proton-vpn-gnome-desktop", "protonvpn-cli"],
                ["sudo", "apt", "autoremove", "-y"],
                ["sudo", "rm", "-f", "/etc/apt/sources.list.d/protonvpn-stable.list"],
                ["sudo", "rm", "-f", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"],
                ["sudo", "find", ".", "-name", "protonvpn-*.deb", "-delete"]
            ]

            for cmd in commands:
                success, error = VPNManager._run_command(cmd)
                if not success and "not found" not in error.lower():
                    return False, error

            return True, "Limpeza concluída"
        except Exception as e:
            return False, str(e)
