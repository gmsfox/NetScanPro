import subprocess
import os
import logging
from typing import Tuple, Optional, List
import re
import requests
import time

class VPNManager:
    # Timeout configurations
    DEFAULT_TIMEOUT = 120
    STATUS_TIMEOUT = 30
    CONNECT_TIMEOUT = 180
    LOGIN_TIMEOUT = 60
    INSTALL_TIMEOUT = 300

    @staticmethod
    def _executar_comando(cmd: List[str], timeout: Optional[int] = None) -> Tuple[bool, str]:
        """Execute commands with robust error handling"""
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
            return False, f"Command timed out ({timeout}s)"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() or f"Command failed with code {e.returncode}"
            return False, error_msg
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _encontrar_executavel() -> Optional[str]:
        """Find ProtonVPN CLI executable path"""
        paths_to_check = [
            "/usr/bin/protonvpn-cli",
            "/usr/local/bin/protonvpn-cli",
            "/opt/protonvpn/protonvpn-cli",
            os.path.expanduser("~/.local/bin/protonvpn-cli")
        ]

        for path in paths_to_check:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path

        # Try finding via which
        success, output = VPNManager._executar_comando(["which", "protonvpn-cli"])
        if success:
            return output.strip()

        return None

    @staticmethod
    def verificar_instalacao() -> bool:
        """Check if ProtonVPN is properly installed"""
        return VPNManager._encontrar_executavel() is not None

    @staticmethod
    def _obter_versao_instalada() -> Tuple[bool, str]:
        """Get installed version"""
        executable = VPNManager._encontrar_executavel()
        if not executable:
            return False, "ProtonVPN CLI not found"

        cmd = [executable, "--version"]
        success, output = VPNManager._executar_comando(cmd)
        if not success:
            return False, output

        version = re.search(r"ProtonVPN-CLI v?(\d+\.\d+\.\d+)", output)
        if version:
            return True, version.group(1)
        return False, "Version not identified"

    @staticmethod
    def _obter_versao_mais_recente() -> Tuple[bool, str]:
        """Get latest available version"""
        try:
            url = "https://repo.protonvpn.com/debian/dists/stable/main/binary-all/"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            versions = re.findall(r'protonvpn-stable-release_(\d+\.\d+\.\d+)_all\.deb', response.text)
            if versions:
                latest = max(versions, key=lambda x: tuple(map(int, x.split('.'))))
                return True, latest
            return False, "Version not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def verificar_atualizacoes() -> Tuple[bool, str]:
        """Check for available updates"""
        success, installed = VPNManager._obter_versao_instalada()
        if not success:
            return False, installed

        success, latest = VPNManager._obter_versao_mais_recente()
        if not success:
            return False, latest

        if installed == latest:
            return False, f"You already have the latest version ({installed})"
        return True, f"New version available: {latest} (current: {installed})"

    @staticmethod
    def instalar() -> Tuple[bool, str]:
        """Complete installation with improved checks"""
        try:
            # Check dependencies
            dependencies = ["wget", "apt-transport-https", "gnupg"]
            for dep in dependencies:
                success, _ = VPNManager._executar_comando(["which", dep])
                if not success:
                    install_cmd = ["sudo", "apt", "install", "-y", dep]
                    success, error = VPNManager._executar_comando(install_cmd)
                    if not success:
                        return False, f"Dependency installation failed: {error}"

            # Configure repository
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
                    return False, f"Configuration failed: {error}"

            # Install client
            install_cmd = ["sudo", "apt", "install", "-y", "protonvpn-cli"]
            success, output = VPNManager._executar_comando(install_cmd, timeout=VPNManager.INSTALL_TIMEOUT)

            if not success:
                return False, f"Installation failed: {output}"

            # Verify installation
            if VPNManager.verificar_instalacao():
                return True, "ProtonVPN CLI installed successfully"
            return False, "Installation appeared successful but executable not found"

        except Exception as e:
            return False, f"Installation error: {str(e)}"

    @staticmethod
    def desinstalar() -> Tuple[bool, str]:
        """Complete uninstallation"""
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
                    logging.warning(f"Command failed during uninstallation: {error}")

            # Verify uninstallation
            if not VPNManager.verificar_instalacao():
                return True, "Uninstallation completed"
            return False, "Uninstallation appeared successful but traces remain"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str]:
        """Improved login method"""
        executable = VPNManager._encontrar_executavel()
        if not executable:
            return False, "ProtonVPN CLI not found"

        try:
            # Method 1: Temporary file
            temp_auth = "/tmp/protonvpn_auth.tmp"
            try:
                with open(temp_auth, "w") as f:
                    f.write(f"{username}\n{password}\n")
                os.chmod(temp_auth, 0o600)

                cmd = ["sudo", executable, "login", "--username-file", temp_auth]
                success, output = VPNManager._executar_comando(cmd, timeout=VPNManager.LOGIN_TIMEOUT)

                if success:
                    return True, "Login successful"

                # Method 2: Interactive fallback
                cmd = f"printf '{username}\\n{password}\\n' | sudo {executable} login"
                success, output = VPNManager._executar_comando(
                    ["bash", "-c", cmd],
                    timeout=VPNManager.LOGIN_TIMEOUT
                )
                if success:
                    return True, "Login successful (alternative method)"

                # Error handling
                if "Invalid credentials" in output:
                    return False, "Invalid credentials"
                elif "timed out" in output:
                    return False, "Timeout - check your connection"
                elif "No internet" in output:
                    return False, "No internet connection"

                return False, output.split("DeprecationWarning")[0].strip()
            finally:
                if os.path.exists(temp_auth):
                    os.remove(temp_auth)
        except Exception as e:
            return False, f"Unexpected login error: {str(e)}"

    @staticmethod
    def conectar() -> Tuple[bool, str]:
        """Connect to VPN with improved handling"""
        executable = VPNManager._encontrar_executavel()
        if not executable:
            return False, "ProtonVPN CLI not found"

        # Check status first
        status_success, status_msg = VPNManager.status()
        if status_success and "Connected" in status_msg:
            return False, "Already connected"

        cmd = ["sudo", executable, "connect", "--fastest"]
        success, output = VPNManager._executar_comando(cmd, timeout=VPNManager.CONNECT_TIMEOUT)

        if success:
            # Verify connection
            time.sleep(3)
            status_success, status_msg = VPNManager.status()
            if status_success and "Connected" in status_msg:
                return True, "Connection established"
            return False, "Appeared successful but status doesn't confirm"

        # Error handling
        if "No internet connection" in output:
            return False, "No internet connection"
        elif "API request failed" in output:
            return False, "ProtonVPN server issues"
        elif "Another connection is active" in output:
            return False, "Another connection is active"

        return False, output

    @staticmethod
    def desconectar() -> Tuple[bool, str]:
        """Disconnect from VPN"""
        executable = VPNManager._encontrar_executavel()
        if not executable:
            return False, "ProtonVPN CLI not found"

        # Check status first
        status_success, status_msg = VPNManager.status()
        if status_success and "Disconnected" in status_msg:
            return False, "Already disconnected"

        cmd = ["sudo", executable, "disconnect"]
        success, output = VPNManager._executar_comando(cmd)

        if success:
            # Verify disconnection
            time.sleep(2)
            status_success, status_msg = VPNManager.status()
            if status_success and "Disconnected" in status_msg:
                return True, "Disconnected successfully"
            return False, "Appeared successful but status doesn't confirm"

        return False, output

    @staticmethod
    def status() -> Tuple[bool, str]:
        """Check connection status with retries"""
        executable = VPNManager._encontrar_executavel()
        if not executable:
            return False, "ProtonVPN CLI not found"

        for attempt in range(3):
            cmd = [executable, "status"]
            success, output = VPNManager._executar_comando(cmd, timeout=VPNManager.STATUS_TIMEOUT)

            if success:
                output_lower = output.lower()
                if "connected" in output_lower:
                    return True, "✅ Connected"
                elif "disconnected" in output_lower:
                    return True, "❌ Disconnected"
                elif "connecting" in output_lower:
                    return True, "🔄 Connecting..."
                return True, output

            time.sleep(2)

        return False, "Failed to check status"