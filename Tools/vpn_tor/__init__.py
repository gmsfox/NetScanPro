# Tools/vpn_tor/__init__.py
from .manager import VPNTorManager
from .installer import VPNTorInstaller

__all__ = ['VPNTorManager', 'VPNTorInstaller']  # Define o que será importado com `from Tools.vpn_tor import *`