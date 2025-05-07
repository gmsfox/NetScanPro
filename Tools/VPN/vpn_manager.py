import subprocess
import logging
import os
import sys
from typing import Tuple

class VPNManager:
    @staticmethod
    def _run_command(cmd: list) -> Tuple[bool, str]:
        """Executa um comando e retorna (success, message)"""
        try:
            result = subprocess.run(cmd, check=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() or "Unknown error"
            return False, error_msg

    @staticmethod
    def check_installation() -> bool:
        """Verifica se o protonvpn-cli está instalado e funcional"""
        success, _ = VPNManager._run_command(["which", "protonvpn-cli"])
        if not success:
            return False

        success, _ = VPNManager._run_command(["protonvpn-cli", "--version"])
        return success

    @staticmethod
    def install() -> Tuple[bool, str]:
        """Instala o ProtonVPN automaticamente"""
        steps = [
            ("Atualizando pacotes", ["sudo", "apt", "update"]),
            ("Instalando dependências", ["sudo", "apt", "install", "-y", "openvpn", "dialog", "python3-pip", "python3-setuptools"]),
            ("Baixando pacote ProtonVPN", ["wget", "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.3_all.deb"]),
            ("Instalando repositório", ["sudo", "dpkg", "-i", "protonvpn-stable-release_1.0.3_all.deb"]),
            ("Atualizando repositórios", ["sudo", "apt", "update"]),
            ("Instalando ProtonVPN", ["sudo", "apt", "install", "-y", "protonvpn"]),
            ("Limpando arquivos", ["rm", "-f", "protonvpn-stable-release_1.0.3_all.deb"])
        ]

        for description, cmd in steps:
            success, message = VPNManager._run_command(cmd)
            if not success:
                return False, f"Falha no passo '{description}': {message}"

        return True, "Instalação concluída com sucesso!"

    @staticmethod
    def connect() -> Tuple[bool, str]:
        return VPNManager._run_command(["protonvpn-cli", "connect", "--fastest"])

    @staticmethod
    def disconnect() -> Tuple[bool, str]:
        return VPNManager._run_command(["protonvpn-cli", "disconnect"])

    @staticmethod
    def status() -> Tuple[bool, str]:
        return VPNManager._run_command(["protonvpn-cli", "status"])
