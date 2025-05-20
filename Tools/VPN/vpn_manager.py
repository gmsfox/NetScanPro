import subprocess
import os
import requests
from typing import Tuple
import logging

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
    def _install_official_package() -> Tuple[bool, str]:
        """Instala seguindo o método oficial da ProtonVPN"""
        try:
            # 1. Baixar pacote .deb
            deb_url = "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.8_all.deb"
            deb_file = "protonvpn-stable-release_1.0.8_all.deb"

            if not os.path.exists(deb_file):
                print("Baixando pacote oficial...")
                response = requests.get(deb_url, timeout=30)
                with open(deb_file, 'wb') as f:
                    f.write(response.content)

            # 2. Instalar seguindo os passos oficiais
            commands = [
                ["sudo", "dpkg", "-i", deb_file],
                ["sudo", "apt", "update", "-y"],
                ["sudo", "apt", "install", "-y", "proton-vpn-gnome-desktop"],
                ["sudo", "apt", "install", "-y", "libayatana-appindicator3-1",
                 "gir1.2-ayatanaappindicator3-0.1", "gnome-shell-extension-appindicator"]
            ]

            for cmd in commands:
                success, error = VPNManager._run_command(cmd)
                if not success:
                    return False, error

            return True, "Instalação oficial concluída com sucesso"

        except Exception as e:
            return False, str(e)

    @staticmethod
    def check_installation() -> bool:
        """Verifica se o ProtonVPN está instalado corretamente"""
        checks = [
            ["which", "protonvpn-cli"],
            ["protonvpn-cli", "--version"],
            ["dpkg", "-l", "proton-vpn-gnome-desktop"]
        ]
        return all(VPNManager._run_command(cmd)[0] for cmd in checks)

    @staticmethod
    def install() -> Tuple[bool, str]:
        """Fluxo completo de instalação"""
        # 1. Remover instalações anteriores
        VPNManager._remove_old_installation()

        # 2. Tentar instalação oficial
        return VPNManager._install_official_package()

    @staticmethod
    def _remove_old_installation() -> Tuple[bool, str]:
        """Remove instalações antigas completamente"""
        try:
            commands = [
                ["sudo", "apt", "remove", "--purge", "-y", "proton-vpn-gnome-desktop"],
                ["sudo", "apt", "autoremove", "-y"],
                ["sudo", "rm", "-f", "/etc/apt/sources.list.d/protonvpn-stable.list"],
                ["sudo", "rm", "-f", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"],
                ["sudo", "find", ".", "-name", "protonvpn-stable-release_*.deb", "-delete"]
            ]

            for cmd in commands:
                VPNManager._run_command(cmd)

            return True, "Remoção concluída"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def connect() -> Tuple[bool, str]:
        """Conecta à VPN"""
        return VPNManager._run_command(["protonvpn-cli", "connect", "--fastest"])

    @staticmethod
    def disconnect() -> Tuple[bool, str]:
        """Desconecta da VPN"""
        return VPNManager._run_command(["protonvpn-cli", "disconnect"])

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verifica status da VPN"""
        return VPNManager._run_command(["protonvpn-cli", "status"])

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Realiza login na VPN"""
        return VPNManager._run_command([
            "protonvpn-cli", "login",
            "--username", username,
            "--password", password
        ])