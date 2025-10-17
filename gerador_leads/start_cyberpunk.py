#!/usr/bin/env python3
"""
🔥 ASIMOV LeadCaptor CYBERPUNK LAUNCHER 🔥
Script de inicialização para a interface terminal cyberpunk
"""

import os
import sys
import subprocess
import importlib.util

def check_and_install_dependencies():
    """Verifica e instala dependências necessárias"""
    # Lista de pacotes: (nome_do_modulo, nome_do_pacote_pip)
    required_packages = [
        ('colorama', 'colorama'),
        ('pyfiglet', 'pyfiglet'),
        ('selenium', 'selenium'),
        ('pandas', 'pandas'),
        ('webdriver_manager', 'webdriver-manager'),
        ('openpyxl', 'openpyxl'),
        ('tqdm', 'tqdm')
    ]
    
    missing_packages = []

    print("🔍 Verificando dependências...")

    for module_name, pip_name in required_packages:
        if importlib.util.find_spec(module_name) is None:
            missing_packages.append(pip_name)
            print(f"❌ {pip_name} não encontrado")
        else:
            print(f"✅ {pip_name} OK")
    
    if missing_packages:
        print(f"\n📦 Instalando {len(missing_packages)} pacotes faltantes...")
        for package in missing_packages:
            try:
                print(f"⬇️  Instalando {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} instalado com sucesso!")
            except subprocess.CalledProcessError:
                print(f"❌ Erro ao instalar {package}")
                return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def main():
    """Função principal do launcher"""
    print("🚀 ASIMOV LeadCaptor CYBERPUNK LAUNCHER")
    print("=" * 50)
    
    # Verificar e instalar dependências
    if not check_and_install_dependencies():
        print("❌ Erro na instalação de dependências!")
        input("Pressione ENTER para sair...")
        return 1
    
    print("\n🎯 Iniciando interface cyberpunk...")
    
    try:
        # Importar e executar a interface cyberpunk
        from cyberpunk_terminal import main as cyberpunk_main
        cyberpunk_main()
    except ImportError as e:
        print(f"❌ Erro ao importar interface cyberpunk: {e}")
        print("Verifique se o arquivo cyberpunk_terminal.py existe.")
        input("Pressione ENTER para sair...")
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        input("Pressione ENTER para sair...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
