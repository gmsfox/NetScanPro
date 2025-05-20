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
        """Executa comandos com tratamento de erros robusto"""
        try:
            resultado = subprocess.run(cmd,
                                    check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    timeout=120)
            return True, resultado.stdout.strip()
        except subprocess.CalledProcessError as e:
            erro = e.stderr.strip() or f"Comando falhou com código {e.returncode}"
            return False, erro
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _obter_versao_mais_recente() -> Tuple[bool, str]:
        """Obtém a versão mais recente disponível"""
        try:
            url = "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/"
            resposta = requests.get(url, timeout=10)
            versoes = re.findall(r'protonvpn-stable-release_(\d+\.\d+\.\d+)_all\.deb', resposta.text)
            if versoes:
                mais_nova = max(versoes, key=lambda x: tuple(map(int, x.split('.'))))
                return True, mais_nova
            return False, "Versão não encontrada"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def verificar_atualizacoes() -> Tuple[bool, str]:
        """Verifica se há atualizações disponíveis"""
        sucesso, instalada = VPNManager._obter_versao_instalada()
        if not sucesso:
            return False, instalada

        sucesso, mais_nova = VPNManager._obter_versao_mais_recente()
        if not sucesso:
            return False, mais_nova

        if instalada == mais_nova:
            return False, f"Você já tem a versão mais recente ({instalada})"
        return True, f"Nova versão disponível: {mais_nova} (atual: {instalada})"

    @staticmethod
    def _obter_versao_instalada() -> Tuple[bool, str]:
        """Obtém a versão instalada"""
        cmd = ["apt-cache", "policy", "protonvpn-stable-release"]
        sucesso, saida = VPNManager._executar_comando(cmd)
        if not sucesso:
            return False, saida

        versao = re.search(r"Instalada: (\d+\.\d+\.\d+)", saida)
        if versao:
            return True, versao.group(1)
        return False, "Versão não identificada"

    @staticmethod
    def verificar_instalacao() -> bool:
        """Verifica se o ProtonVPN está instalado"""
        verificacoes = [
            ["which", "protonvpn-cli"],
            ["which", "proton-vpn-gnome-desktop"],
            ["dpkg", "-l", "protonvpn-stable-release"]
        ]
        return any(VPNManager._executar_comando(cmd)[0] for cmd in verificacoes)

    @staticmethod
    def instalar() -> Tuple[bool, str]:
        """Instalação completa"""
        # 1. Configurar repositório
        comandos_repo = [
            ["sudo", "wget", "-O", "/usr/share/keyrings/protonvpn-archive-keyring.gpg",
             "https://repo.protonvpn.com/debian/public_key.asc"],
            ["sudo", "sh", "-c",
             "echo 'deb [arch=all signed-by=/usr/share/keyrings/protonvpn-archive-keyring.gpg] https://repo.protonvpn.com/debian stable main' > /etc/apt/sources.list.d/protonvpn-stable.list"],
            ["sudo", "apt", "update"]
        ]

        for cmd in comandos_repo:
            sucesso, erro = VPNManager._executar_comando(cmd)
            if not sucesso:
                return False, f"Falha ao configurar repositório: {erro}"

        # 2. Instalar cliente
        clientes = ["proton-vpn-gnome-desktop", "protonvpn-cli"]
        instalado = False
        mensagem = ""

        for cliente in clientes:
            sucesso, erro = VPNManager._executar_comando(["sudo", "apt", "install", "-y", cliente])
            if sucesso:
                instalado = True
                mensagem = f"Cliente {cliente} instalado com sucesso"
                break
            mensagem = erro

        if not instalado:
            return False, f"Falha ao instalar ambos clientes: {mensagem}"

        return True, mensagem

    @staticmethod
    def desinstalar() -> Tuple[bool, str]:
        """Desinstalação completa"""
        comandos = [
            ["sudo", "apt", "remove", "--purge", "-y", "proton-vpn-gnome-desktop", "protonvpn-cli"],
            ["sudo", "rm", "-f", "/etc/apt/sources.list.d/protonvpn-stable.list"],
            ["sudo", "rm", "-f", "/usr/share/keyrings/protonvpn-archive-keyring.gpg"],
            ["sudo", "apt", "autoremove", "-y"],
            ["sudo", "rm", "-rf", os.path.expanduser("~/.config/protonvpn")]
        ]

        erros = []
        for cmd in comandos:
            sucesso, erro = VPNManager._executar_comando(cmd)
            if not sucesso and "não encontrado" not in erro.lower():
                erros.append(erro)

        if erros:
            return False, " | ".join(erros)
        return True, "Desinstalação concluída com sucesso"

    @staticmethod
    def conectar() -> Tuple[bool, str]:
        """Conectar à VPN"""
        clientes = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for cliente in clientes:
            sucesso, _ = VPNManager._executar_comando(["which", cliente])
            if sucesso:
                return VPNManager._executar_comando(["sudo", cliente, "connect", "--fastest"])
        return False, "Nenhum cliente ProtonVPN instalado"

    @staticmethod
    def desconectar() -> Tuple[bool, str]:
        """Desconectar da VPN"""
        clientes = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for cliente in clientes:
            sucesso, _ = VPNManager._executar_comando(["which", cliente])
            if sucesso:
                return VPNManager._executar_comando(["sudo", cliente, "disconnect"])
        return False, "Nenhum cliente ProtonVPN instalado"

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Verificar status da conexão"""
        clientes = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for cliente in clientes:
            sucesso, _ = VPNManager._executar_comando(["which", cliente])
            if sucesso:
                return VPNManager._executar_comando([cliente, "status"])
        return False, "Nenhum cliente ProtonVPN instalado"

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Configurar credenciais de login"""
        clientes = ["protonvpn-cli", "proton-vpn-gnome-desktop"]
        for cliente in clientes:
            sucesso, _ = VPNManager._executar_comando(["which", cliente])
            if sucesso:
                cmd = f"printf '{username}\\n{password}\\n' | sudo {cliente} login"
                return VPNManager._executar_comando(["bash", "-c", cmd])
        return False, "Nenhum cliente ProtonVPN instalado"
