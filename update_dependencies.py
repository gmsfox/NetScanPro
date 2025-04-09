import subprocess
import sys
import platform
import os

def run_command(cmd):
    """Executa um comando de forma segura no terminal."""
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Erro ao executar: {cmd}")
        print(e)

def atualizar_dependencias():
    print("=" * 50)
    print("     NetScan Pro - Atualizando Dependências")
    print("=" * 50)

    # Etapa 1: Instalar dependências principais do projeto
    print("\n[1] Instalando colorama e numlookupapi...")
    run_command(f"{sys.executable} -m pip install colorama numlookupapi")

    # Etapa 2: Garantir que pipreqs está instalado
    print("\n[2] Instalando pipreqs...")
    run_command(f"{sys.executable} -m pip install pipreqs")

    # Etapa 3: Gerar requirements.txt com encoding UTF-8
    print("\n[3] Gerando requirements.txt com pipreqs...")
    run_command(f"{sys.executable} -m pipreqs . --force --encoding=utf-8")

    print("\n[✔] requirements.txt atualizado com sucesso!")

if __name__ == "__main__":
    atualizar_dependencias()
