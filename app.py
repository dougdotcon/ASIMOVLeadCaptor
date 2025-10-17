#!/usr/bin/env python3
"""
🔥 ASIMOV LeadCaptor - Launcher Principal 🔥
Sistema completo de captura e envio de leads com WhatsApp
"""

import os
import sys
import subprocess
import threading
import time
import signal
import importlib.util
from pathlib import Path

class ASIMOVLeadCaptor:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.gerador_dir = self.root_dir / "gerador_leads"
        self.disparador_dir = self.root_dir / "disparador"
        self.processes = []
        self.running = True
        
    def print_banner(self):
        """Exibe o banner principal"""
        banner = """
╔════════════════════════════════════════════════════════════════════╗
║                🔥 ASIMOV LeadCaptor - Sistema Completo             ║
║                    Captura + Envio de Leads Automatizado           ║
╠════════════════════════════════════════════════════════════════════╣
║  🎯 Gerador de Leads: Google Maps Scraping                        ║
║  📱 Disparador WhatsApp: Envio em massa inteligente               ║
║  🤖 IA Integrada: Mensagens únicas para cada contato              ║
╚════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def check_dependencies(self):
        """Verifica se as dependências estão instaladas"""
        print("🔍 Verificando dependências do sistema...")
        
        # Verificar Python
        if sys.version_info < (3, 7):
            print("❌ Python 3.7+ é necessário!")
            return False
            
        # Verificar Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js: {result.stdout.strip()}")
            else:
                print("❌ Node.js não encontrado!")
                return False
        except FileNotFoundError:
            print("❌ Node.js não encontrado!")
            return False
            
        # Verificar dependências Python
        python_deps = [
            ('colorama', 'colorama'),
            ('pyfiglet', 'pyfiglet'),
            ('selenium', 'selenium'),
            ('pandas', 'pandas'),
            ('webdriver_manager', 'webdriver-manager'),
            ('openpyxl', 'openpyxl'),
            ('tqdm', 'tqdm')
        ]
        
        missing_python = []
        for module_name, pip_name in python_deps:
            if importlib.util.find_spec(module_name) is None:
                missing_python.append(pip_name)
                print(f"❌ Python: {pip_name} não encontrado")
            else:
                print(f"✅ Python: {pip_name} OK")
                
        # Verificar dependências Node.js
        print("\n🔍 Verificando dependências Node.js...")
        if not (self.disparador_dir / "node_modules").exists():
            print("❌ Node.js: Dependências não instaladas")
            print("💡 Executando npm install...")
            try:
                subprocess.run(['npm', 'install'], cwd=self.disparador_dir, check=True)
                print("✅ Dependências Node.js instaladas!")
            except subprocess.CalledProcessError:
                print("❌ Erro ao instalar dependências Node.js")
                return False
        else:
            print("✅ Node.js: Dependências OK")
            
        # Instalar dependências Python faltantes
        if missing_python:
            print(f"\n📦 Instalando {len(missing_python)} pacotes Python...")
            for package in missing_python:
                try:
                    print(f"⬇️  Instalando {package}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"✅ {package} instalado!")
                except subprocess.CalledProcessError:
                    print(f"❌ Erro ao instalar {package}")
                    return False
                    
        print("✅ Todas as dependências verificadas!")
        return True
        
    def show_menu(self):
        """Exibe o menu principal"""
        menu = """
╔════════════════════════════════════════════════════════════════════╗
║                        🎯 Menu Principal                           ║
╠════════════════════════════════════════════════════════════════════╣
║  [1] 🚀 Iniciar Sistema Completo (Gerador + Disparador)           ║
║  [2] 🎯 Apenas Gerador de Leads (Google Maps)                     ║
║  [3] 📱 Apenas Disparador WhatsApp                                ║
║  [4] ⚙️  Configurações e Status                                    ║
║  [5] 📚 Documentação e Ajuda                                      ║
║  [0] 🚪 Sair                                                       ║
╚════════════════════════════════════════════════════════════════════╝
        """
        print(menu)
        
    def start_gerador_leads(self):
        """Inicia o gerador de leads em thread separada"""
        def run_gerador():
            try:
                print("🎯 Iniciando Gerador de Leads...")
                os.chdir(self.gerador_dir)
                
                # Importar e executar o cyberpunk terminal
                sys.path.insert(0, str(self.gerador_dir))
                from cyberpunk_terminal import main as cyberpunk_main
                cyberpunk_main()
                
            except Exception as e:
                print(f"❌ Erro no Gerador de Leads: {e}")
                
        thread = threading.Thread(target=run_gerador, daemon=True)
        thread.start()
        return thread
        
    def start_disparador_whatsapp(self):
        """Inicia o disparador WhatsApp"""
        def run_disparador():
            try:
                print("📱 Iniciando Disparador WhatsApp...")
                os.chdir(self.disparador_dir)
                
                # Executar o sistema Node.js
                process = subprocess.Popen(
                    ['node', 'index.js'],
                    cwd=self.disparador_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                self.processes.append(process)
                
                # Mostrar output em tempo real
                for line in iter(process.stdout.readline, ''):
                    if line and self.running:
                        print(f"📱 WhatsApp: {line.strip()}")
                        
            except Exception as e:
                print(f"❌ Erro no Disparador WhatsApp: {e}")
                
        thread = threading.Thread(target=run_disparador, daemon=True)
        thread.start()
        return thread
        
    def start_complete_system(self):
        """Inicia o sistema completo"""
        print("🚀 Iniciando Sistema Completo ASIMOV LeadCaptor...")
        print("=" * 60)
        
        # Iniciar gerador de leads
        gerador_thread = self.start_gerador_leads()
        time.sleep(2)  # Aguardar inicialização
        
        # Iniciar disparador WhatsApp
        disparador_thread = self.start_disparador_whatsapp()
        
        print("\n✅ Sistema Completo Iniciado!")
        print("🎯 Gerador de Leads: Ativo")
        print("📱 Disparador WhatsApp: Ativo")
        print("\n💡 Instruções:")
        print("   1. Use o terminal cyberpunk para capturar leads")
        print("   2. O WhatsApp será conectado automaticamente")
        print("   3. Use /menu no WhatsApp para ver comandos")
        print("   4. Pressione Ctrl+C para parar o sistema")
        
        try:
            # Manter o sistema rodando
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()
            
    def start_only_gerador(self):
        """Inicia apenas o gerador de leads"""
        print("🎯 Iniciando apenas Gerador de Leads...")
        os.chdir(self.gerador_dir)
        
        try:
            sys.path.insert(0, str(self.gerador_dir))
            from cyberpunk_terminal import main as cyberpunk_main
            cyberpunk_main()
        except Exception as e:
            print(f"❌ Erro: {e}")
            
    def start_only_disparador(self):
        """Inicia apenas o disparador WhatsApp"""
        print("📱 Iniciando apenas Disparador WhatsApp...")
        os.chdir(self.disparador_dir)
        
        try:
            subprocess.run(['node', 'index.js'], cwd=self.disparador_dir)
        except KeyboardInterrupt:
            print("\n⏹️  Disparador WhatsApp interrompido.")
        except Exception as e:
            print(f"❌ Erro: {e}")
            
    def show_status(self):
        """Mostra status e configurações"""
        status = f"""
╔════════════════════════════════════════════════════════════════════╗
║                    ⚙️ Status e Configurações                       ║
╠════════════════════════════════════════════════════════════════════╣
║  📁 Diretório Raiz: {str(self.root_dir)[:45]}...║
║  🎯 Gerador: {str(self.gerador_dir.exists()).ljust(45)} ║
║  📱 Disparador: {str(self.disparador_dir.exists()).ljust(41)} ║
║                                                                    ║
║  📋 Arquivos de Configuração:                                     ║
║     • gerador_leads/requirements.txt                              ║
║     • disparador/package.json                                     ║
║     • disparador/key.json                                         ║
║                                                                    ║
║  🔧 Para configurar APIs:                                         ║
║     • Veja: disparador/CONFIGURAR_API.md                         ║
╚════════════════════════════════════════════════════════════════════╝
        """
        print(status)
        
        # Verificar configurações
        key_file = self.disparador_dir / "key.json"
        if key_file.exists():
            print("✅ Arquivo de configuração encontrado")
        else:
            print("⚠️  Arquivo key.json não encontrado")
            
        input("\nPressione ENTER para continuar...")
        
    def show_help(self):
        """Mostra documentação e ajuda"""
        help_text = """
╔════════════════════════════════════════════════════════════════════╗
║                        📚 Documentação                            ║
╠════════════════════════════════════════════════════════════════════╣
║  📖 Arquivos de Documentação:                                     ║
║     • disparador/README.md - Guia completo do disparador          ║
║     • disparador/CONFIGURAR_API.md - Configuração de APIs         ║
║     • disparador/STATUS_SISTEMA.md - Status do sistema            ║
║                                                                    ║
║  🎯 Como Usar:                                                     ║
║     1. Execute o sistema completo (opção 1)                       ║
║     2. Use o terminal cyberpunk para capturar leads               ║
║     3. Configure APIs para mensagens únicas (opcional)            ║
║     4. Use comandos WhatsApp para envio em massa                  ║
║                                                                    ║
║  📱 Comandos WhatsApp Principais:                                 ║
║     • /menu - Ver todos os comandos                               ║
║     • /mass - Sistema de envio em massa                           ║
║     • /testeenvio [número] [mensagem] - Teste rápido             ║
║     • /stats - Estatísticas de envio                             ║
║                                                                    ║
║  🔧 Suporte:                                                       ║
║     • Verifique os logs em caso de erro                          ║
║     • Reinicie o sistema se necessário                           ║
║     • Configure APIs para funcionalidades completas              ║
╚════════════════════════════════════════════════════════════════════╝
        """
        print(help_text)
        input("\nPressione ENTER para continuar...")
        
    def shutdown(self):
        """Encerra todos os processos"""
        print("\n⏹️  Encerrando ASIMOV LeadCaptor...")
        self.running = False
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
                
        print("✅ Sistema encerrado com sucesso!")
        
    def run(self):
        """Executa o launcher principal"""
        # Configurar handler para Ctrl+C
        signal.signal(signal.SIGINT, lambda s, f: self.shutdown())
        
        self.print_banner()
        
        # Verificar dependências
        if not self.check_dependencies():
            print("❌ Erro nas dependências! Corrija e tente novamente.")
            input("Pressione ENTER para sair...")
            return 1
            
        # Loop principal do menu
        while self.running:
            try:
                self.show_menu()
                choice = input("Escolha uma opção: ").strip()
                
                if choice == '1':
                    self.start_complete_system()
                elif choice == '2':
                    self.start_only_gerador()
                elif choice == '3':
                    self.start_only_disparador()
                elif choice == '4':
                    self.show_status()
                elif choice == '5':
                    self.show_help()
                elif choice == '0':
                    break
                else:
                    print("❌ Opção inválida! Tente novamente.")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
                
        self.shutdown()
        return 0

def main():
    """Função principal"""
    launcher = ASIMOVLeadCaptor()
    return launcher.run()

if __name__ == "__main__":
    sys.exit(main())
