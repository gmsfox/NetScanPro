import subprocess
import os
import logging
from typing import Tuple, Optional
import re
import requests
from pathlib import Path
import time

class VPNManager:
    # Configuração de timeouts
    DEFAULT_TIMEOUT = 120
    STATUS_TIMEOUT = 30
    CONNECT_TIMEOUT = 180
    LOGIN_TIMEOUT = 60
    INSTALL_TIMEOUT = 300

    @staticmethod
    def _executar_comando(cmd: list, timeout: Optional[int] = None) -> Tuple[bool, str]:
        """Executa comandos com tratamento robusto de erros"""
        timeout = timeout or VPNManager.DEFAULT_TIMEOUT
        try:
            result = subprocess.run(cmd,
                                  check=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=timeout)
            return True, result.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, f"O comando excedeu o tempo limite ({timeout}s)"
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
            response = requests.get(url, timeout=15)
            response.raise_for_status()
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
            ["dpkg", "-l", "protonvpn-stable-release"]
        ]
        return any(VPNManager._executar_comando(cmd)[0] for cmd in checks)

    @staticmethod
    def instalar() -> Tuple[bool, str]:
        """Instalação completa com tratamento aprimorado"""
        try:
            # 1. Configurar repositório
            repo_cmds = [
                ["sudo", "wget", "-O", "/usr/share/keyrings/protonvpn-archive-keyring.gpg",
                 "https://repo.protonvpn.com/debian/public_key.asc"],
                ["sudo", "sh", "-c",
                 "echo 'deb [arch=all signed-by=/usr/share/keyrings/protonvpn-archive-keyring.gpg] https://repo.protonvpn.com/debian stable main' > /etc/apt/sources.list.d/protonvpn-stable.list"],
                ["sudo", "apt", "update", "-y"]
            ]

            for cmd in repo_cmds:
                success, error = VPNManager._executar_comando(cmd, timeout=VPNManager.INSTALL_TIMEOUT)
                if not success:
                    return False, f"Falha na configuração: {error}"

            # 2. Instalar cliente
            clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
            for client in clients:
                success, error = VPNManager._executar_comando(
                    ["sudo", "apt", "install", "-y", client],
                    timeout=VPNManager.INSTALL_TIMEOUT
                )
                if success:
                    # Verificar se a instalação foi realmente bem-sucedida
                    if VPNManager.verificar_instalacao():
                        return True, f"{client} instalado com sucesso"
                    return False, f"{client} aparentemente instalado mas verificação falhou"

            return False, "Falha ao instalar ambos clientes"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def desinstalar() -> Tuple[bool, str]:
        """Desinstalação completa"""
        try:
            cmds = [
                ["sudo", "apt", "remove", "--purge", "-y", "proton-vpn-gnome-desktop", "protonvpn-cli"],
                ["sudo", "rm", "-f", "/etc/apt/sources.list.d/protonvpn-stable.list"],
                ["sudo", "rm", "-f", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"],
                ["sudo", "apt", "autoremove", "-y"],
                ["sudo", "rm", "-rf", os.path.expanduser("~/.config/protonvpn")]
            ]

            for cmd in cmds:
                success, error = VPNManager._executar_comando(cmd, timeout=VPNManager.DEFAULT_TIMEOUT)
                if not success:
                    logging.warning(f"Comando falhou durante desinstalação: {error}")

            # Verificar se foi realmente desinstalado
            if not VPNManager.verificar_instalacao():
                return True, "Desinstalação concluída"
            return False, "Desinstalação aparentemente concluída mas vestígios permanecem"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Método de login aprimorado"""
        try:
            # Método 1: Arquivo temporário
            temp_auth = "/tmp/protonvpn_auth.tmp"
            try:
                with open(temp_auth, "w") as f:
                    f.write(f"{username}\n{password}\n")
                os.chmod(temp_auth, 0o600)

                cmd = ["sudo", "protonvpn-cli", "login", "--username-file", temp_auth]
                success, output = VPNManager._executar_comando(cmd, timeout=VPNManager.LOGIN_TIMEOUT)

                if success:
                    return True, "Login realizado com sucesso"

                # Método 2: Fallback interativo
                cmd = f"printf '{username}\\n{password}\\n' | sudo protonvpn-cli login"
                success, output = VPNManager._executar_comando(
                    ["bash", "-c", cmd],
                    timeout=VPNManager.LOGIN_TIMEOUT
                )
                if success:
                    return True, "Login realizado (método alternativo)"

                # Tratamento de erros específicos
                if "Invalid credentials" in output:
                    return False, "Credenciais inválidas"
                elif "timed out" in output:
                    return False, "Tempo limite excedido - verifique sua conexão"
                elif "No internet" in output:
                    return False, "Sem conexão com a internet"

                return False, output.split("DeprecationWarning")[0].strip()
            finally:
                if os.path.exists(temp_auth):
                    os.remove(temp_auth)
        except Exception as e:
            return False, f"Erro inesperado durante login: {str(e)}"

    @staticmethod
    def conectar() -> Tuple[bool, str]:
        """Conectar à VPN com tratamento melhorado"""
        # Verificar status primeiro
        status_success, status_msg = VPNManager.status()
        if status_success and "Conectado" in status_msg:
            return False, "Já conectado"

        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for client in clients:
            # Verificar qual cliente está disponível
            which_success, _ = VPNManager._executar_comando(["which", client])
            if not which_success:
                continue

            # Comando específico para cada cliente
            if client == "protonvpn-cli":
                cmd = ["sudo", "protonvpn-cli", "connect", "--fastest"]
            else:
                cmd = ["proton-vpn-gnome-desktop", "--connect"]

            success, output = VPNManager._executar_comando(cmd, timeout=VPNManager.CONNECT_TIMEOUT)

            if success:
                # Verificar se realmente conectou
                time.sleep(3)  # Esperar conexão estabilizar
                status_success, status_msg = VPNManager.status()
                if status_success and "Conectado" in status_msg:
                    return True, "Conexão estabelecida com sucesso"
                return False, "Conexão aparentemente bem-sucedida mas status não confirma"

            # Tratamento de erros específicos
            if "No internet connection" in output:
                return False, "Sem conexão com a internet"
            elif "API request failed" in output:
                return False, "Problema nos servidores ProtonVPN"
            elif "Another connection is active" in output:
                return False, "Já existe uma conexão ativa"

        return False, "Falha ao conectar em todos os clientes"

    @staticmethod
    def desconectar() -> Tuple[bool, str]:
        """Desconectar da VPN"""
        # Verificar status primeiro
        status_success, status_msg = VPNManager.status()
        if status_success and "Desconectado" in status_msg:
            return False, "Já desconectado"

        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for client in clients:
            which_success, _ = VPNManager._executar_comando(["which", client])
            if which_success:
                success, output = VPNManager._executar_comando(
                    ["sudo", client, "disconnect"],
                    timeout=VPNManager.DEFAULT_TIMEOUT
                )
                if success:
                    # Verificar se realmente desconectou
                    time.sleep(2)
                    status_success, status_msg = VPNManager.status()
                    if status_success and "Desconectado" in status_msg:
                        return True, "Desconectado com sucesso"
                    return False, "Desconexão aparentemente bem-sucedida mas status não confirma"

        return False, "Nenhum cliente ProtonVPN instalado ou respondendo"

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verificar status da conexão com tentativas"""
        clients = ["protonvpn-cli", "proton-vpn-gnome-desktop"]

        for client in clients:
            # Verificar qual cliente está disponível
            which_success, _ = VPNManager._executar_comando(["which", client])
            if not which_success:
                continue

            # Tentar obter status (3 tentativas)
            for attempt in range(3):
                success, output = VPNManager._executar_comando(
                    [client, "status"],
                    timeout=VPNManager.STATUS_TIMEOUT
                )

                if success:
                    # Processar saída para formato mais limpo
                    output_lower = output.lower()
                    if "connected" in output_lower or "conectado" in output_lower:
                        return True, "✅ Conectado"
                    elif "disconnected" in output_lower or "desconectado" in output_lower:
                        return True, "❌ Desconectado"
                    elif "connecting" in output_lower:
                        return True, "🔄 Conectando..."
                    return True, output

                time.sleep(2)  # Espera entre tentativas

        return False, "Nenhum cliente ProtonVPN respondendo corretamente"