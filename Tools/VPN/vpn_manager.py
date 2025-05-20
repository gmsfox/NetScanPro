import subprocess
import os
import logging
from typing import Tuple
import re
import requests
from pathlib import Path

class VPNManager:
    @staticmethod
    def _executar_comando(cmd: list) -> Tuple[bool, str]:
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
            error_msg = e.stderr.strip() or f"Comando falhou com código {e.returncode}"
            return False, error_msg
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _obter_versao_mais_recente() -> Tuple[bool, str]:
        """Obtém a versão mais recente disponível"""
        try:
            url = "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/"
            response = requests.get(url, timeout=10)
            versions = re.findall(r'protonvpn-stable-release_(\d+\.\d+\.\d+)_all\.deb', response.text)
            if versions:
                latest = max(versions, key=lambda x: tuple(map(int, x.split('.'))))
                return True, latest
            return False, "Versão não encontrada"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def verificar_atualizacoes() -> Tuple[bool, str]:
        """Verifica se há atualizações disponíveis"""
        success, installed = VPNManager._obter_versao_instalada()
        if not success:
            return False, installed

        success, latest = VPNManager._obter_versao_mais_recente()
        if not success:
            return False, latest

        if installed == latest:
            return False, f"Você já tem a versão mais recente ({installed})"
        return True, f"Nova versão disponível: {latest} (atual: {installed})"

    @staticmethod
    def _obter_versao_instalada() -> Tuple[bool, str]:
        """Obtém a versão instalada"""
        cmd = ["apt-cache", "policy", "protonvpn-stable-release"]
        success, output = VPNManager._executar_comando(cmd)
        if not success:
            return False, output

        version = re.search(r"Instalada: (\d+\.\d+\.\d+)", output)
        if version:
            return True, version.group(1)
        return False, "Versão não identificada"

    @staticmethod
    def verificar_instalacao() -> bool:
        """Verifica se o ProtonVPN está instalado"""
        checks = [
            ["which", "protonvpn-cli"],
            ["which", "proton-vpn-gnome-desktop"],
            ["dpkg", "-l", "protonvpn-stable-release"]
        ]
        return any(VPNManager._executar_comando(cmd)[0] for cmd in checks)

    @staticmethod
    def instalar() -> Tuple[bool, str]:
        """Instalação completa"""
        # 1. Configurar repositório
        repo_cmds = [
            ["sudo", "wget", "-O", "/usr/share/keyrings/protonvpn-archive-keyring.gpg",
             "https://repo.protonvpn.com/debian/public_key.asc"],
            ["sudo", "sh", "-c",
             "echo 'deb [arch=all signed-by=/usr/share/keyrings/protonvpn-archive-keyring.gpg] https://repo.protonvpn.com/debian stable main' > /etc/apt/sources.list.d/protonvpn-stable.list"],
            ["sudo", "apt", "update"]
        ]

        for cmd in repo_cmds:
            success, error = VPNManager._executar_comando(cmd)
            if not success:
                return False, f"Falha ao configurar repositório: {error}"

        # 2. Instalar cliente
        clients = ["proton-vpn-gnome-desktop", "protonvpn-cli"]
        installed = False
        message = ""

        for client in clients:
            success, error = VPNManager._executar_comando(["sudo", "apt", "install", "-y", client])
            if success:
                installed = True
                message = f"Cliente {client} instalado com sucesso"
                break
            message = error

        if not installed:
            return False, f"Falha ao instalar ambos clientes: {message}"

        return True, message

    @staticmethod
    def desinstalar() -> Tuple[bool, str]:
        """Desinstalação completa"""
        cmds = [
            ["sudo", "apt", "remove", "--purge", "-y", "proton-vpn-gnome-desktop", "protonvpn-cli"],
            ["sudo", "rm", "-f", "/etc/apt/sources.list.d/protonvpn-stable.list"],
            ["sudo", "rm", "-f", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"],
            ["sudo", "apt", "autoremove", "-y"],
            ["sudo", "rm", "-rf", os.path.expanduser("~/.config/protonvpn")]
        ]

        errors = []
        for cmd in cmds:
            success, error = VPNManager._executar_comando(cmd)
            if not success and "não encontrado" not in error.lower():
                errors.append(error)

        if errors:
            return False, " | ".join(errors)
        return True, "Desinstalação concluída com sucesso"

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Configura login de forma robusta"""
        try:
            # Método 1: Usando arquivo temporário seguro
            temp_auth = "/tmp/protonvpn_auth.tmp"
            with open(temp_auth, "w") as f:
                f.write(f"{username}\n{password}\n")
            os.chmod(temp_auth, 0o600)

            cmd = ["sudo", "protonvpn-cli", "login", "--username-file", temp_auth]
            success, output = VPNManager._executar_comando(cmd)

            # Limpeza imediata
            os.remove(temp_auth)

            if success:
                return True, "Login realizado com sucesso"

            # Método 2: Fallback para input interativo
            if "DeprecationWarning" in output:
                cmd = f"printf '{username}\\n{password}\\n' | sudo protonvpn-cli login"
                return VPNManager._executar_comando(["bash", "-c", cmd])

            return False, output.split("DeprecationWarning")[0].strip()

        except Exception as e:
            if 'temp_auth' in locals() and os.path.exists(temp_auth):
                os.remove(temp_auth)
            return False, str(e)

    @staticmethod
    def conectar() -> Tuple[bool, str]:
        """Conecta à VPN"""
        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for client in clients:
            success, _ = VPNManager._executar_comando(["which", client])
            if success:
                return VPNManager._executar_comando(["sudo", client, "connect", "--fastest"])
        return False, "Nenhum cliente ProtonVPN instalado"

    @staticmethod
    def desconectar() -> Tuple[bool, str]:
        """Desconecta da VPN"""
        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for client in clients:
            success, _ = VPNManager._executar_comando(["which", client])
            if success:
                return VPNManager._executar_comando(["sudo", client, "disconnect"])
        return False, "Nenhum cliente ProtonVPN instalado"

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verifica status da conexão"""
        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for client in clients:
            success, _ = VPNManager._executar_comando(["which", client])
            if success:
                return VPNManager._executar_comando([client, "status"])
        return False, "Nenhum cliente ProtonVPN instalado"