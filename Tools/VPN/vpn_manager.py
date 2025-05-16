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
        """Instala o ProtonVPN com tratamento completo de erros"""
        try:
            # 1. Instalar dependências necessárias
            deps = [
                ["sudo", "apt", "update"],
                ["sudo", "apt", "install", "-y", "wget", "gnupg2", "software-properties-common"]
            ]

            for cmd in deps:
                success, msg = VPNManager._run_command(cmd)
                if not success:
                    return False, f"Erro instalando dependências: {msg}"

            # 2. Adicionar chave GPG manualmente
            gpg_commands = [
                ["wget", "-qO-", "https://repo.protonvpn.com/debian/public_key.asc"],
                ["sudo", "gpg", "--dearmor", "-o", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"]
            ]

            for cmd in gpg_commands:
                success, msg = VPNManager._run_command(cmd)
                if not success:
                    return False, f"Erro configurando chave GPG: {msg}"

            # 3. Configurar repositório
            repo_cmd = [
                "sudo", "sh", "-c",
                'echo "deb [arch=all signed-by=/usr/share/keyrings/protonvpn-archive-keyring.gpg] '
                'https://repo.protonvpn.com/debian stable main" > '
                '/etc/apt/sources.list.d/protonvpn-stable.list'
            ]

            success, msg = VPNManager._run_command(repo_cmd)
            if not success:
                return False, f"Erro configurando repositório: {msg}"

            # 4. Instalação final
            install_steps = [
                ["sudo", "apt", "update"],
                ["sudo", "apt", "install", "-y", "protonvpn"]
            ]

            for cmd in install_steps:
                success, msg = VPNManager._run_command(cmd)
                if not success:
                    return False, f"Erro na instalação: {msg}"

            return True, "Instalação concluída com sucesso!"

        except Exception as e:
            logging.error("Erro crítico durante instalação: %s", str(e))
            return False, f"Erro crítico: {str(e)}"

    @staticmethod
    def connect() -> Tuple[bool, str]:
        return VPNManager._run_command(["protonvpn-cli", "connect", "--fastest"])

    @staticmethod
    def disconnect() -> Tuple[bool, str]:
        return VPNManager._run_command(["protonvpn-cli", "disconnect"])

    @staticmethod
    def status() -> Tuple[bool, str]:
        return VPNManager._run_command(["protonvpn-cli", "status"])
