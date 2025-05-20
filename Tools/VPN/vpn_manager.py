import subprocess
import os
import sys
from typing import Tuple
import logging
import requests

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
    def check_installation() -> bool:
        """Verifica se o ProtonVPN CLI está instalado"""
        checks = [
            ["which", "protonvpn-cli"],
            ["protonvpn-cli", "--version"]
        ]
        return all(VPNManager._run_command(cmd)[0] for cmd in checks)

    @staticmethod
    def install() -> Tuple[bool, str]:
        """Instalação via pip + configuração inicial"""
        try:
            # 1. Instalar dependências
            deps_cmd = [
                "sudo", "apt", "install", "-y",
                "openvpn", "dialog", "python3-pip",
                "python3-setuptools", "wireguard-tools"
            ]
            success, error = VPNManager._run_command(deps_cmd)
            if not success:
                return False, f"Dependências falharam: {error}"

            # 2. Instalar via pip
            pip_cmd = ["sudo", "pip3", "install", "--upgrade", "protonvpn-cli"]
            success, error = VPNManager._run_command(pip_cmd)
            if not success:
                return False, f"Instalação pip falhou: {error}"

            # 3. Configurar CLI
            if not os.path.exists("/usr/local/bin/protonvpn-cli"):
                return False, "Binário não encontrado após instalação"

            return True, "ProtonVPN CLI instalado com sucesso"

        except Exception as e:
            return False, f"Erro crítico: {str(e)}"

    @staticmethod
    def init_config(username: str, password: str) -> Tuple[bool, str]:
        """Configuração inicial do ProtonVPN"""
        try:
            cmd = f"printf '{username}\\n{password}\\n' | sudo protonvpn-cli --init"
            success, error = VPNManager._run_command(["bash", "-c", cmd])
            return success, error
        except Exception as e:
            return False, str(e)

    @staticmethod
    def connect() -> Tuple[bool, str]:
        """Conecta à VPN"""
        return VPNManager._run_command(["sudo", "protonvpn-cli", "connect", "--fastest"])

    @staticmethod
    def disconnect() -> Tuple[bool, str]:
        """Desconecta da VPN"""
        return VPNManager._run_command(["sudo", "protonvpn-cli", "disconnect"])

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verifica status da VPN"""
        return VPNManager._run_command(["sudo", "protonvpn-cli", "status"])

    @staticmethod
    def cleanup():
        """Remove arquivos temporários"""
        try:
            cmds = [
                ["sudo", "pip3", "uninstall", "-y", "protonvpn-cli"],
                ["sudo", "rm", "-f", "/usr/local/bin/protonvpn-cli"],
                ["sudo", "rm", "-rf", "~/.protonvpn"]
            ]
            for cmd in cmds:
                VPNManager._run_command(cmd)
        except Exception:
            pass