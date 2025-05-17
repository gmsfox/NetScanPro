import subprocess
import logging
import os
import re
import requests
from typing import Tuple

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
                                  timeout=30)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() or f"Command failed with code {e.returncode}"
            return False, error_msg
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _get_latest_deb_version() -> Tuple[bool, str]:
        """Obtém a última versão do pacote .deb do repositório"""
        try:
            repo_url = "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/"
            response = requests.get(repo_url, timeout=10)
            response.raise_for_status()

            deb_versions = re.findall(
                r'protonvpn-stable-release_(\d+\.\d+\.\d+)_all\.deb',
                response.text
            )

            if not deb_versions:
                return False, "No .deb packages found in repository"

            latest = max(deb_versions, key=lambda x: tuple(map(int, x.split('.'))))
            return True, latest

        except Exception as e:
            logging.error(f"Version check failed: {str(e)}")
            return False, str(e)

    @staticmethod
    def _download_deb_package(version: str) -> Tuple[bool, str]:
        """Baixa o pacote .deb específico"""
        try:
            deb_url = f"https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_{version}_all.deb"
            local_file = f"protonvpn-stable-release_{version}_all.deb"

            with requests.get(deb_url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(local_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return True, local_file
        except Exception as e:
            logging.error(f"Download failed: {str(e)}")
            return False, str(e)

    @staticmethod
    def check_installation() -> bool:
        """Verificação robusta da instalação"""
        checks = [
            ["which", "protonvpn-cli"],
            ["protonvpn-cli", "--version"],
            ["dpkg", "-l", "protonvpn"]
        ]

        for cmd in checks:
            success, _ = VPNManager._run_command(cmd)
            if not success:
                return False
        return True

    @staticmethod
    def install() -> Tuple[bool, str]:
        """Instalação completa com gerenciamento de versões"""
        # Obter última versão
        success, version = VPNManager._get_latest_deb_version()
        if not success:
            return False, f"Failed to determine latest version: {version}"

        # Baixar pacote
        success, deb_file = VPNManager._download_deb_package(version)
        if not success:
            return False, f"Failed to download package: {deb_file}"

        # Sequência de instalação
        steps = [
            ("Installing dependencies", ["sudo", "apt", "install", "-y", "gnupg", "wget"]),
            ("Adding GPG key", ["wget", "-qO-", "https://repo.protonvpn.com/debian/public_key.asc",
                              "|", "sudo", "gpg", "--dearmor",
                              "-o", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"]),
            ("Installing package", ["sudo", "dpkg", "-i", deb_file]),
            ("Fixing dependencies", ["sudo", "apt", "--fix-broken", "install"]),
            ("Updating repositories", ["sudo", "apt", "update"]),
            ("Installing ProtonVPN", ["sudo", "apt", "install", "-y", "protonvpn"])
        ]

        for step_name, cmd in steps:
            success, error = VPNManager._run_command(cmd)
            if not success:
                return False, f"{step_name} failed: {error}"

        return True, f"Successfully installed ProtonVPN {version}"

    @staticmethod
    def cleanup():
        """Remove arquivos .deb antigos"""
        try:
            for f in os.listdir('.'):
                if f.startswith('protonvpn-stable-release_') and f.endswith('.deb'):
                    os.remove(f)
        except Exception as e:
            logging.warning(f"Cleanup failed: {str(e)}")

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