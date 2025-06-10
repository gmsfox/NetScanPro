import subprocess
import os
import logging
from typing import Tuple, Optional, List
import re
import requests
import time

class VPNManager:
    # Configurações de timeout
    DEFAULT_TIMEOUT = 120
    STATUS_TIMEOUT = 30
    CONNECT_TIMEOUT = 180
    LOGIN_TIMEOUT = 60
    INSTALL_TIMEOUT = 300

    @staticmethod
    def _encontrar_executavel() -> Optional[str]:
        """Encontra o caminho absoluto do protonvpn-cli"""
        paths = [
            "/usr/bin/protonvpn-cli",
            "/usr/local/bin/protonvpn-cli",
            "/opt/protonvpn/protonvpn-cli",
            os.path.expanduser("~/.local/bin/protonvpn-cli")
        ]

        for path in paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path

        # Tenta encontrar via which
        success, output = subprocess.getstatusoutput("which protonvpn-cli")
        if success == 0:
            return output.strip()

        return None

    @staticmethod
    def _executar_comando(cmd: List[str], timeout: Optional[int] = None) -> Tuple[bool, str]:
        """Executa comandos com auto-instalação do protonvpn-cli se necessário"""
        # Verifica se é um comando do protonvpn-cli
        if len(cmd) > 0 and ("protonvpn-cli" in cmd[0] or "protonvpn-cli" in str(cmd)):
            cli_path = VPNManager._encontrar_executavel()
            if not cli_path:
                # Instala automaticamente se não encontrado
                install_success, install_msg = VPNManager.instalar()
                if not install_success:
                    return False, f"Falha na instalação automática: {install_msg}"
                cli_path = VPNManager._encontrar_executavel()
                if not cli_path:
                    return False, "ProtonVPN CLI ainda não encontrado após instalação"

            # Substitui pelo caminho absoluto
            if "protonvpn-cli" in cmd[0]:
                cmd[0] = cli_path
            else:
                cmd[cmd.index("protonvpn-cli")] = cli_path

        # Executa o comando
        timeout = timeout or VPNManager.DEFAULT_TIMEOUT
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
            return True, result.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, f"Timeout após {timeout}s"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() or f"Erro {e.returncode}"
            return False, error_msg
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"

    @staticmethod
    def verificar_instalacao() -> bool:
        """Verifica se o ProtonVPN está instalado"""
        return VPNManager._encontrar_executavel() is not None

    @staticmethod
    def _obter_versao_instalada() -> Tuple[bool, str]:
        """Obtém a versão instalada"""
        cli_path = VPNManager._encontrar_executavel()
        if not cli_path:
            return False, "ProtonVPN CLI não encontrado"

        cmd = [cli_path, "--version"]
        success, output = VPNManager._executar_comando(cmd)
        if not success:
            return False, output

        version = re.search(r"ProtonVPN-CLI v?(\d+\.\d+\.\d+)", output)
        if version:
            return True, version.group(1)
        return False, "Versão não identificada"

    @staticmethod
    def _obter_versao_mais_recente() -> Tuple[bool, str]:
        """Obtém a versão mais recente"""
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
        """Verifica atualizações disponíveis"""
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
    def instalar() -> Tuple[bool, str]:
        """Instala o ProtonVPN CLI automaticamente"""
        try:
            # 1. Configura repositório
            repo_cmds = [
                ["sudo", "wget", "-qO", "/usr/share/keyrings/protonvpn-archive-keyring.gpg",
                 "https://repo.protonvpn.com/debian/public_key.asc"],
                ["sudo", "chmod", "644", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"],
                ["sudo", "sh", "-c",
                 "echo 'deb [arch=all signed-by=/usr/share/keyrings/protonvpn-archive-keyring.gpg] https://repo.protonvpn.com/debian stable main' > /etc/apt/sources.list.d/protonvpn-stable.list"],
                ["sudo", "apt", "update"]
            ]

            for cmd in repo_cmds:
                success, error = VPNManager._executar_comando(cmd)
                if not success:
                    return False, f"Falha na configuração: {error}"

            # 2. Instala o pacote
            install_cmd = ["sudo", "apt", "install", "-y", "protonvpn-cli"]
            success, output = VPNManager._executar_comando(install_cmd, timeout=VPNManager.INSTALL_TIMEOUT)

            if not success:
                return False, f"Falha na instalação: {output}"

            # 3. Verifica instalação
            if VPNManager.verificar_instalacao():
                return True, "ProtonVPN CLI instalado com sucesso"
            return False, "Instalação aparentemente bem-sucedida mas executável não encontrado"

        except Exception as e:
            return False, f"Erro durante instalação: {str(e)}"

    @staticmethod
    def desinstalar() -> Tuple[bool, str]:
        """Desinstala completamente"""
        try:
            cmds = [
                ["sudo", "apt", "remove", "--purge", "-y", "protonvpn-cli"],
                ["sudo", "rm", "-f", "/etc/apt/sources.list.d/protonvpn-stable.list"],
                ["sudo", "rm", "-f", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"],
                ["sudo", "apt", "autoremove", "-y"],
                ["sudo", "rm", "-rf", os.path.expanduser("~/.config/protonvpn")]
            ]

            for cmd in cmds:
                success, error = VPNManager._executar_comando(cmd)
                if not success:
                    logging.warning(f"Comando falhou durante desinstalação: {error}")

            if not VPNManager.verificar_instalacao():
                return True, "Desinstalação concluída"
            return False, "Desinstalação aparentemente concluída mas vestígios permanecem"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Login na VPN"""
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

                # Tratamento de erros
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
        """Conecta à VPN"""
        # Verifica status primeiro
        status_success, status_msg = VPNManager.status()
        if status_success and "Conectado" in status_msg:
            return False, "Já conectado"

        cmd = ["sudo", "protonvpn-cli", "connect", "--fastest"]
        success, output = VPNManager._executar_comando(cmd, timeout=VPNManager.CONNECT_TIMEOUT)

        if success:
            # Verifica conexão
            time.sleep(3)
            status_success, status_msg = VPNManager.status()
            if status_success and "Conectado" in status_msg:
                return True, "Conexão estabelecida com sucesso"
            return False, "Conexão aparentemente bem-sucedida mas status não confirma"

        # Tratamento de erros
        if "No internet connection" in output:
            return False, "Sem conexão com a internet"
        elif "API request failed" in output:
            return False, "Problema nos servidores ProtonVPN"
        elif "Another connection is active" in output:
            return False, "Já existe uma conexão ativa"

        return False, output

    @staticmethod
    def desconectar() -> Tuple[bool, str]:
        """Desconecta da VPN"""
        # Verifica status primeiro
        status_success, status_msg = VPNManager.status()
        if status_success and "Desconectado" in status_msg:
            return False, "Já desconectado"

        cmd = ["sudo", "protonvpn-cli", "disconnect"]
        success, output = VPNManager._executar_comando(cmd)

        if success:
            # Verifica desconexão
            time.sleep(2)
            status_success, status_msg = VPNManager.status()
            if status_success and "Desconectado" in status_msg:
                return True, "Desconectado com sucesso"
            return False, "Desconexão aparentemente bem-sucedida mas status não confirma"

        return False, output

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verifica status da conexão"""
        cmd = ["protonvpn-cli", "status"]
        success, output = VPNManager._executar_comando(cmd, timeout=VPNManager.STATUS_TIMEOUT)

        if success:
            output_lower = output.lower()
            if "connected" in output_lower or "conectado" in output_lower:
                return True, "✅ Conectado"
            elif "disconnected" in output_lower or "desconectado" in output_lower:
                return True, "❌ Desconectado"
            elif "connecting" in output_lower:
                return True, "🔄 Conectando..."
            return True, output

        return False, "Falha ao verificar status"