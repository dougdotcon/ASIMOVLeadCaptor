#!/usr/bin/env python3
"""
🔥 ASIMOV LeadCaptor - Inicializador do Sistema WhatsApp 🔥
Script para configurar e testar o sistema de mensagens WhatsApp integrado
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    print("""
🔥 ASIMOV LeadCaptor - Sistema WhatsApp 🔥
==========================================
    """)

def check_node_js():
    """Verifica se Node.js está instalado"""
    print("📦 Verificando Node.js...")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js encontrado: {version}")
            
            # Verificar se a versão é compatível (>= 16)
            version_num = int(version.replace('v', '').split('.')[0])
            if version_num >= 16:
                return True
            else:
                print(f"❌ Versão {version} é muito antiga. Instale Node.js 16 ou superior.")
                return False
        else:
            print("❌ Node.js não encontrado!")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar Node.js: {e}")
        return False

def install_dependencies():
    """Instala as dependências do Node.js"""
    whatsapp_dir = Path(__file__).parent / 'whatsapp_sender'
    
    print("📦 Instalando dependências do WhatsApp Sender...")
    
    if not whatsapp_dir.exists():
        print(f"❌ Diretório {whatsapp_dir} não encontrado!")
        return False
    
    try:
        result = subprocess.run(
            ['npm', 'install'],
            cwd=whatsapp_dir,
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso!")
            return True
        else:
            print(f"❌ Erro ao instalar dependências:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def setup_env_file():
    """Configura o arquivo .env"""
    whatsapp_dir = Path(__file__).parent / 'whatsapp_sender'
    env_example = whatsapp_dir / '.env.example'
    env_file = whatsapp_dir / '.env'
    
    if not env_file.exists():
        if env_example.exists():
            print("⚙️ Criando arquivo .env...")
            
            # Copiar .env.example para .env
            with open(env_example, 'r') as example:
                content = example.read()
            
            with open(env_file, 'w') as env:
                env.write(content)
            
            print(f"✅ Arquivo .env criado em: {env_file}")
            
            # Solicitar API key do usuário
            print("\n🔑 Configuração da API OpenRouter")
            print("=" * 40)
            print("1. Acesse: https://openrouter.ai")
            print("2. Crie uma conta gratuita")
            print("3. Obtenha sua API key")
            print("4. Cole abaixo (ou pressione ENTER para configurar depois)")
            
            api_key = input("\nSua API key OpenRouter: ").strip()
            
            if api_key and api_key != "":
                # Atualizar o arquivo .env com a API key
                with open(env_file, 'r') as f:
                    content = f.read()
                
                content = content.replace('seu_openrouter_api_key_aqui', api_key)
                
                with open(env_file, 'w') as f:
                    f.write(content)
                
                print("✅ API key configurada!")
            else:
                print("⚠️ API key não configurada. Configure depois no arquivo .env")
        else:
            print(f"❌ Arquivo .env.example não encontrado!")
            return False
    else:
        print("✅ Arquivo .env já existe")
    
    return True

def run_tests():
    """Executa os testes do sistema"""
    whatsapp_dir = Path(__file__).parent / 'whatsapp_sender'
    
    print("🧪 Executando testes do sistema...")
    
    try:
        result = subprocess.run(
            ['node', 'test_sender.js'],
            cwd=whatsapp_dir,
            shell=True
        )
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False

def start_whatsapp_sender():
    """Inicia o WhatsApp Sender"""
    whatsapp_dir = Path(__file__).parent / 'whatsapp_sender'
    
    print("🚀 Iniciando WhatsApp Sender...")
    print("📱 IMPORTANTE: Prepare seu celular para escanear o QR Code!")
    
    input("\nPressione ENTER quando estiver pronto...")
    
    try:
        # Abrir em nova janela
        if os.name == 'nt':  # Windows
            subprocess.Popen(f'start cmd /k "cd /d {whatsapp_dir} && node whatsapp_sender.js"', shell=True)
        else:  # Linux/Mac
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'cd {whatsapp_dir} && node whatsapp_sender.js'])
        
        print("✅ WhatsApp Sender aberto em nova janela!")
        print("📱 Escaneie o QR Code com seu WhatsApp")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar WhatsApp Sender: {e}")
        return False

def start_main_system():
    """Inicia o sistema principal cyberpunk"""
    print("🎯 Iniciando sistema principal ASIMOV...")
    
    try:
        subprocess.run([sys.executable, 'start_cyberpunk.py'])
    except Exception as e:
        print(f"❌ Erro ao iniciar sistema principal: {e}")

def main():
    """Função principal"""
    print_banner()
    
    print("🔍 Este script irá:")
    print("1. Verificar Node.js")
    print("2. Instalar dependências")
    print("3. Configurar arquivo .env")
    print("4. Executar testes")
    print("5. Iniciar WhatsApp Sender")
    print("6. Iniciar sistema principal")
    
    input("\nPressione ENTER para continuar...")
    
    # Passo 1: Verificar Node.js
    if not check_node_js():
        print("\n❌ Instale Node.js 16+ primeiro:")
        print("https://nodejs.org/")
        return False
    
    # Passo 2: Instalar dependências
    if not install_dependencies():
        print("\n❌ Falha na instalação das dependências")
        return False
    
    # Passo 3: Configurar .env
    if not setup_env_file():
        print("\n❌ Falha na configuração do arquivo .env")
        return False
    
    # Passo 4: Executar testes
    print("\n" + "="*50)
    if not run_tests():
        print("\n⚠️ Alguns testes falharam, mas você pode tentar continuar")
        continuar = input("Deseja continuar mesmo assim? (s/n): ")
        if not continuar.lower().startswith('s'):
            return False
    
    # Passo 5: Pergunta o que fazer
    print("\n" + "="*50)
    print("🎯 Sistema configurado com sucesso!")
    print("\nOpções:")
    print("[1] Iniciar apenas WhatsApp Sender")
    print("[2] Iniciar sistema completo (recomendado)")
    print("[0] Sair")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == "1":
        start_whatsapp_sender()
    elif choice == "2":
        print("\n🚀 Iniciando sistema completo...")
        time.sleep(2)
        start_main_system()
    else:
        print("👋 Sistema configurado! Execute start_cyberpunk.py quando quiser usar.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Configuração concluída com sucesso!")
        else:
            print("\n❌ Configuração falhou. Verifique os erros acima.")
    except KeyboardInterrupt:
        print("\n\n⚠️ Configuração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")