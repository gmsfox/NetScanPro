import subprocess
import logging
import os
import re
import requests
from typing import Tuple
import glob

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
    def _find_installed_version() -> Tuple[bool, str]:
        """Verifica qual versão está instalada no sistema"""
        try:
            # Verifica via dpkg
            success, output = VPNManager._run_command(["dpkg", "-l", "protonvpn"])
            if success and "protonvpn" in output:
                version = re.search(r'protonvpn\s+(\d+\.\d+\.\d+)', output)
                if version:
                    return True, version.group(1)

            # Verifica via protonvpn-cli
            success, output = VPNManager._run_command(["protonvpn-cli", "--version"])
            if success:
                version = re.search(r'Version:\s+(\d+\.\d+\.\d+)', output)
                if version:
                    return True, version.group(1)

            return False, "ProtonVPN not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _clean_old_deb_files(current_version: str) -> Tuple[bool, str]:
        """Remove arquivos .deb antigos da pasta do NetScanPro"""
        try:
            deb_files = glob.glob('protonvpn-stable-release_*_all.deb')
            removed = []

            for deb_file in deb_files:
                # Extrai a versão do nome do arquivo
                version_match = re.search(r'protonvpn-stable-release_(\d+\.\d+\.\d+)_all\.deb', deb_file)
                if version_match:
                    file_version = version_match.group(1)
                    if file_version != current_version:
                        os.remove(deb_file)
                        removed.append(file_version)

            if removed:
                return True, f"Removed old versions: {', '.join(removed)}"
            return True, "No old versions found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _remove_old_installation() -> Tuple[bool, str]:
        """Remove completamente instalações antigas do ProtonVPN"""
        try:
            commands = [
                ["sudo", "apt", "remove", "--purge", "-y", "protonvpn"],
                ["sudo", "apt", "autoremove", "-y"],
                ["sudo", "rm", "-f", "/etc/apt/sources.list.d/protonvpn-stable.list"],
                ["sudo", "rm", "-f", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"],
                ["sudo", "rm", "-f", "/usr/local/bin/protonvpn"],
                ["sudo", "rm", "-rf", "/var/lib/protonvpn"]
            ]

            for cmd in commands:
                VPNManager._run_command(cmd)

            return True, "Old installation completely removed"
        except Exception as e:
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
        # 1. Remover instalações antigas
        success, message = VPNManager._remove_old_installation()
        if not success:
            logging.warning(f"Failed to remove old installation: {message}")

        # 2. Obter última versão
        success, version = VPNManager._get_latest_deb_version()
        if not success:
            return False, f"Failed to determine latest version: {version}"

        # 3. Baixar pacote
        success, deb_file = VPNManager._download_deb_package(version)
        if not success:
            return False, f"Failed to download package: {deb_file}"

        # 4. Limpar arquivos .deb antigos
        VPNManager._clean_old_deb_files(version)

        # 5. Sequência de instalação
        steps = [
            ("Installing dependencies", ["sudo", "apt", "install", "-y", "gnupg", "wget", "gpg"]),
            ("Downloading GPG key", ["sudo", "wget", "-qO", "/usr/share/keyrings/protonvpn-archive-keyring.gpg",
                                   "https://repo.protonvpn.com/debian/public_key.asc"]),
            ("Setting key permissions", ["sudo", "chmod", "644", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"]),
            ("Installing package", ["sudo", "dpkg", "-i", deb_file]),
            ("Fixing dependencies", ["sudo", "apt", "--fix-broken", "install", "-y"]),
            ("Updating repositories", ["sudo", "apt", "update", "-y"]),
            ("Installing ProtonVPN", ["sudo", "apt", "install", "-y", "protonvpn"])
        ]

        for step_name, cmd in steps:
            success, error = VPNManager._run_command(cmd)
            if not success:
                VPNManager.cleanup()
                return False, f"{step_name} failed: {error}"

        return True, f"Successfully installed ProtonVPN {version}"

    @staticmethod
    def cleanup():
        """Remove arquivos temporários"""
        try:
            # Remove todos os arquivos .deb da pasta atual
            for f in glob.glob('protonvpn-stable-release_*_all.deb'):
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