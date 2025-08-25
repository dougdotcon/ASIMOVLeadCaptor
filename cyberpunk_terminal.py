#!/usr/bin/env python3
"""
🔥 ASIMOV LeadCaptor CYBERPUNK TERMINAL 🔥
Interface Terminal Cyberpunk ASCII para Captura de Leads
Desenvolvido para substituir a GUI tradicional
"""

import os
import sys
import time
import threading
from datetime import datetime
import colorama
from colorama import Fore, Back, Style
import pyfiglet
from google_maps_integration import main_query
from constants import ESTADOS_BRASILEIROS
from bairros_brasileiros import BAIRROS_POR_ESTADO
from constants_usa import ESTADOS_AMERICANOS
from cidades_americanas import CIDADES_POR_ESTADO_USA

# Inicializar colorama para Windows
colorama.init()

class CyberpunkTerminal:
    def __init__(self):
        self.running = True
        self.current_operation = None
        
    def clear_screen(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Exibe o banner cyberpunk ASCII"""
        self.clear_screen()
        
        # Banner principal
        banner = pyfiglet.figlet_format("ASIMOV", font="slant")
        print(f"{Fore.CYAN}{Style.BRIGHT}{banner}{Style.RESET_ALL}")

        # Subtítulo cyberpunk
        print(f"{Fore.GREEN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    ▓▓▓ ASIMOV LeadCaptor TERMINAL v2.0 ▓▓▓{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'═' * 80}{Style.RESET_ALL}")
        
        # Arte ASCII cyberpunk
        ascii_art = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║   █████╗ ███████╗██╗███╗   ███╗ ██████╗ ██╗   ██╗                        ║
    ║  ██╔══██╗██╔════╝██║████╗ ████║██╔═══██╗██║   ██║                        ║
    ║  ███████║███████╗██║██╔████╔██║██║   ██║██║   ██║                        ║
    ║  ██╔══██║╚════██║██║██║╚██╔╝██║██║   ██║╚██╗ ██╔╝                        ║
    ║  ██║  ██║███████║██║██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝                         ║
    ║  ╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚═╝ ╚═════╝   ╚═══╝                          ║
    ║                    LeadCaptor Neural System                              ║
    ╚══════════════════════════════════════════════════════════════════════════╝
        """
        print(f"{Fore.MAGENTA}{ascii_art}{Style.RESET_ALL}")
        
        # Status do sistema
        print(f"{Fore.GREEN}[SISTEMA ONLINE]{Style.RESET_ALL} {Fore.CYAN}Neural Network Activated{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[CONEXÃO]{Style.RESET_ALL} {Fore.CYAN}Matrix Interface Ready{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[TIMESTAMP]{Style.RESET_ALL} {Fore.YELLOW}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'═' * 80}{Style.RESET_ALL}")
    
    def print_menu(self):
        """Exibe o menu principal cyberpunk"""
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                           MENU PRINCIPAL                                 ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[1]{Style.RESET_ALL} {Fore.YELLOW}► INICIAR CAPTURA DE LEADS{Style.RESET_ALL}                                  {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[2]{Style.RESET_ALL} {Fore.YELLOW}► CONFIGURAÇÕES AVANÇADAS{Style.RESET_ALL}                                  {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[3]{Style.RESET_ALL} {Fore.YELLOW}► STATUS DO SISTEMA{Style.RESET_ALL}                                        {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[4]{Style.RESET_ALL} {Fore.YELLOW}► HISTÓRICO DE OPERAÇÕES{Style.RESET_ALL}                                  {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}[0]{Style.RESET_ALL} {Fore.RED}► DESCONECTAR DO SISTEMA{Style.RESET_ALL}                                   {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    def get_user_input(self, prompt, input_type="string"):
        """Obtém entrada do usuário com estilo cyberpunk"""
        while True:
            try:
                print(f"\n{Fore.GREEN}┌─[{Fore.CYAN}ASIMOV{Fore.GREEN}]─[{Fore.YELLOW}INPUT{Fore.GREEN}]{Style.RESET_ALL}")
                user_input = input(f"{Fore.GREEN}└──╼ {Fore.CYAN}{prompt}{Style.RESET_ALL} {Fore.GREEN}►{Style.RESET_ALL} ")
                
                if input_type == "int":
                    return int(user_input)
                elif input_type == "choice":
                    if user_input in ['0', '1', '2', '3', '4']:
                        return user_input
                    else:
                        self.print_error("Opção inválida! Digite 0, 1, 2, 3 ou 4.")
                        continue
                else:
                    return user_input.strip()
            except ValueError:
                self.print_error(f"Entrada inválida! Digite um {input_type} válido.")
            except KeyboardInterrupt:
                self.print_warning("\nOperação cancelada pelo usuário.")
                return None
    
    def print_success(self, message):
        """Exibe mensagem de sucesso"""
        print(f"{Fore.GREEN}[✓ SUCESSO]{Style.RESET_ALL} {message}")
    
    def print_error(self, message):
        """Exibe mensagem de erro"""
        print(f"{Fore.RED}[✗ ERRO]{Style.RESET_ALL} {message}")
    
    def print_warning(self, message):
        """Exibe mensagem de aviso"""
        print(f"{Fore.YELLOW}[⚠ AVISO]{Style.RESET_ALL} {message}")
    
    def print_info(self, message):
        """Exibe mensagem informativa"""
        print(f"{Fore.CYAN}[ℹ INFO]{Style.RESET_ALL} {message}")
    
    def print_loading_animation(self, message, duration=3):
        """Exibe animação de carregamento cyberpunk"""
        chars = "▓▒░"
        for i in range(duration * 10):
            char = chars[i % len(chars)]
            print(f"\r{Fore.GREEN}[{char * 3}]{Style.RESET_ALL} {Fore.CYAN}{message}{Style.RESET_ALL} {Fore.GREEN}[{char * 3}]{Style.RESET_ALL}", end="")
            time.sleep(0.1)
        print(f"\r{Fore.GREEN}[✓]{Style.RESET_ALL} {Fore.CYAN}{message}{Style.RESET_ALL} {Fore.GREEN}[COMPLETO]{Style.RESET_ALL}")
    
    def show_estados_menu(self):
        """Exibe menu de seleção de estados"""
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        SELEÇÃO DE ESTADO                                 ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Exibir estados em colunas
        estados_list = list(ESTADOS_BRASILEIROS.keys())
        for i, estado in enumerate(estados_list, 1):
            if i % 3 == 1:
                print(f"{Fore.GREEN}[{i:2d}]{Style.RESET_ALL} {Fore.YELLOW}{estado:<20}{Style.RESET_ALL}", end="")
            elif i % 3 == 2:
                print(f" {Fore.GREEN}[{i:2d}]{Style.RESET_ALL} {Fore.YELLOW}{estado:<20}{Style.RESET_ALL}", end="")
            else:
                print(f" {Fore.GREEN}[{i:2d}]{Style.RESET_ALL} {Fore.YELLOW}{estado:<20}{Style.RESET_ALL}")
        
        if len(estados_list) % 3 != 0:
            print()
        
        while True:
            try:
                escolha = self.get_user_input("Digite o número do estado", "int")
                if escolha and 1 <= escolha <= len(estados_list):
                    return estados_list[escolha - 1]
                else:
                    self.print_error(f"Número inválido! Digite entre 1 e {len(estados_list)}.")
            except:
                self.print_error("Entrada inválida!")

    def show_pais_menu(self):
        """Exibe menu de seleção de país"""
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        SELEÇÃO DE PAÍS                                   ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        print(f"\n{Fore.YELLOW}🌎 PAÍSES DISPONÍVEIS:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'─' * 75}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} {Fore.YELLOW}🇧🇷 Brasil{Style.RESET_ALL} - 27 estados, 270 bairros")
        print(f"{Fore.GREEN}[2]{Style.RESET_ALL} {Fore.YELLOW}🇺🇸 Estados Unidos{Style.RESET_ALL} - 51 estados, 510 cidades")
        print(f"{Fore.GREEN}{'─' * 75}{Style.RESET_ALL}")

        while True:
            try:
                escolha = self.get_user_input("Digite o número do país", "int")

                if escolha == 1:
                    return "Brasil"
                elif escolha == 2:
                    return "Estados Unidos"
                else:
                    self.print_error("Número inválido! Digite 1 para Brasil ou 2 para Estados Unidos.")

            except:
                self.print_error("Entrada inválida!")

    def show_estados_menu_por_pais(self, pais):
        """Exibe menu de seleção de estados baseado no país"""
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        SELEÇÃO DE ESTADO                                 ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                           {pais:<43} ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        if pais == "Brasil":
            estados_dict = ESTADOS_BRASILEIROS
            flag = "🇧🇷"
        else:  # Estados Unidos
            estados_dict = ESTADOS_AMERICANOS
            flag = "🇺🇸"

        estados_list = list(estados_dict.keys())

        print(f"\n{Fore.YELLOW}{flag} ESTADOS DISPONÍVEIS:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'─' * 75}{Style.RESET_ALL}")

        # Exibir estados em colunas
        for i, estado in enumerate(estados_list, 1):
            if i % 3 == 1:
                print(f"{Fore.GREEN}[{i:2d}]{Style.RESET_ALL} {Fore.YELLOW}{estado:<20}{Style.RESET_ALL}", end="")
            elif i % 3 == 2:
                print(f" {Fore.GREEN}[{i:2d}]{Style.RESET_ALL} {Fore.YELLOW}{estado:<20}{Style.RESET_ALL}", end="")
            else:
                print(f" {Fore.GREEN}[{i:2d}]{Style.RESET_ALL} {Fore.YELLOW}{estado:<20}{Style.RESET_ALL}")

        if len(estados_list) % 3 != 0:
            print()

        print(f"{Fore.GREEN}{'─' * 75}{Style.RESET_ALL}")

        while True:
            try:
                escolha = self.get_user_input("Digite o número do estado", "int")
                if escolha and 1 <= escolha <= len(estados_list):
                    return estados_list[escolha - 1]
                else:
                    self.print_error(f"Número inválido! Digite entre 1 e {len(estados_list)}.")
            except:
                self.print_error("Entrada inválida!")

    def show_bairros_menu(self, estado, pais="Brasil"):
        """Exibe menu de seleção de bairros/cidades do estado ou permite digitação livre"""
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        SELEÇÃO DE BAIRRO/CIDADE                          ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                           {estado:<43} ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        # Selecionar fonte de dados baseada no país
        if pais == "Brasil":
            bairros = BAIRROS_POR_ESTADO.get(estado, [])
            tipo_local = "BAIRROS"
            flag = "🇧🇷"
        else:  # Estados Unidos
            bairros = CIDADES_POR_ESTADO_USA.get(estado, [])
            tipo_local = "CIDADES"
            flag = "🇺🇸"

        if bairros:
            print(f"\n{Fore.YELLOW}{flag} PRINCIPAIS {tipo_local} SUGERIDOS:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'─' * 75}{Style.RESET_ALL}")

            # Exibir bairros/cidades em 2 colunas
            for i in range(0, len(bairros), 2):
                linha = ""
                for j in range(2):
                    if i + j < len(bairros):
                        local = bairros[i + j]
                        numero = i + j + 1
                        linha += f"{Fore.GREEN}[{numero:2d}]{Style.RESET_ALL} {Fore.YELLOW}{local:<35}{Style.RESET_ALL}"
                print(linha)

            print(f"\n{Fore.MAGENTA}[0] ► DIGITAR OUTRO {tipo_local[:-1]}/CIDADE{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'─' * 75}{Style.RESET_ALL}")

            while True:
                try:
                    escolha = self.get_user_input(f"Digite o número do {tipo_local.lower()[:-1]} ou [0] para digitar outro", "int")

                    if escolha == 0:
                        # Usuário quer digitar outro local
                        local_digitado = self.get_user_input(f"Digite o nome do {tipo_local.lower()[:-1]}/cidade")
                        if local_digitado and local_digitado.strip():
                            return local_digitado.strip()
                        else:
                            self.print_error(f"Nome do {tipo_local.lower()[:-1]} não pode estar vazio!")
                    elif escolha and 1 <= escolha <= len(bairros):
                        local_selecionado = bairros[escolha - 1]
                        # Para Brasil, extrair nome do bairro (remover cidade entre parênteses)
                        # Para EUA, usar nome da cidade diretamente
                        if pais == "Brasil":
                            local_nome = local_selecionado.split(' (')[0]
                        else:
                            local_nome = local_selecionado
                        return local_nome
                    else:
                        self.print_error(f"Número inválido! Digite entre 0 e {len(bairros)}.")

                except:
                    self.print_error("Entrada inválida!")
        else:
            # Se não há locais cadastrados para o estado, permitir digitação livre
            print(f"\n{Fore.YELLOW}📍 Digite o nome do {tipo_local.lower()[:-1]}/cidade de {estado}:{Style.RESET_ALL}")
            local_digitado = self.get_user_input(f"Nome do {tipo_local.lower()[:-1]}/cidade")
            if local_digitado and local_digitado.strip():
                return local_digitado.strip()
            else:
                self.print_error(f"Nome do {tipo_local.lower()[:-1]} não pode estar vazio!")
                return self.show_bairros_menu(estado, pais)  # Tentar novamente

    def capture_leads_interface(self):
        """Interface para captura de leads"""
        self.print_banner()
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                      CONFIGURAÇÃO DE CAPTURA                             ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        # Seleção do país
        pais = self.show_pais_menu()
        self.print_success(f"País selecionado: {pais}")

        # Seleção do estado
        estado = self.show_estados_menu_por_pais(pais)
        self.print_success(f"Estado selecionado: {estado}")

        # Seleção do bairro/cidade
        local = self.show_bairros_menu(estado, pais)
        if not local:
            return
        tipo_local = "Bairro" if pais == "Brasil" else "Cidade"
        self.print_success(f"{tipo_local} selecionado: {local}")
        
        # Entrada da palavra-chave
        palavra_chave = self.get_user_input("Digite a palavra-chave (ex: restaurante, dentista)")
        if not palavra_chave:
            return
        
        # Entrada da quantidade
        quantidade = self.get_user_input("Digite a quantidade de leads", "int")
        if not quantidade or quantidade <= 0:
            self.print_error("Quantidade deve ser maior que zero!")
            return
        
        # Confirmação
        print(f"\n{Fore.YELLOW}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║                        CONFIRMAÇÃO DE DADOS                              ║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        flag = "🇧🇷" if pais == "Brasil" else "🇺🇸"
        print(f"{Fore.GREEN}País:{Style.RESET_ALL} {Fore.CYAN}{flag} {pais}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Estado:{Style.RESET_ALL} {Fore.CYAN}{estado}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{tipo_local}:{Style.RESET_ALL} {Fore.CYAN}{local}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Palavra-chave:{Style.RESET_ALL} {Fore.CYAN}{palavra_chave}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Quantidade:{Style.RESET_ALL} {Fore.CYAN}{quantidade}{Style.RESET_ALL}")

        confirmar = self.get_user_input("Confirmar operação? (s/n)")
        if confirmar and confirmar.lower() in ['s', 'sim', 'y', 'yes']:
            self.execute_capture(pais, estado, local, palavra_chave, quantidade)
        else:
            self.print_warning("Operação cancelada.")
    
    def execute_capture(self, pais, estado, local, palavra_chave, quantidade):
        """Executa a captura de leads"""
        print(f"\n{Fore.RED}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.RED}║                        INICIANDO OPERAÇÃO                                ║{Style.RESET_ALL}")
        print(f"{Fore.RED}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Animação de inicialização
        self.print_loading_animation("Inicializando sistema neural", 2)
        self.print_loading_animation("Conectando ao Google Maps", 2)
        self.print_loading_animation("Configurando parâmetros de busca", 1)
        
        # Preparar parâmetros baseados no país
        if pais == "Brasil":
            search_term = f"{palavra_chave} {local} {estado}"
            location_term = f"{local}, {estado}"
        else:  # Estados Unidos
            search_term = f"{palavra_chave} {local} {estado}"
            location_term = f"{local}, {estado}, USA"

        save_dir = "./resultados"
        
        # Criar diretório se não existir
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"\n{Fore.GREEN}[OPERAÇÃO INICIADA]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Termo de busca:{Style.RESET_ALL} {search_term}")
        print(f"{Fore.CYAN}Meta de leads:{Style.RESET_ALL} {quantidade}")
        print(f"{Fore.CYAN}Diretório de saída:{Style.RESET_ALL} {save_dir}")
        
        # Callback para atualizações de status
        def status_callback(message):
            # Filtrar mensagens para exibir apenas as importantes
            if any(keyword in message for keyword in ["[INFO]", "[SUCESSO]", "[ERRO]", "[NAVEGAÇÃO"]):
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"{Fore.GREEN}[{timestamp}]{Style.RESET_ALL} {message}")
        
        try:
            # Executar captura
            result = main_query(
                search_for=search_term,
                total=quantidade,
                location=location_term,
                save_dir=save_dir,
                file_format="excel",
                headless_mode=True,
                callback=status_callback
            )
            
            if result:
                self.print_success(f"Operação concluída! {len(result)} leads capturados.")
                self.print_info(f"Arquivo salvo em: {save_dir}")
            else:
                self.print_warning("Nenhum lead foi encontrado.")
                
        except Exception as e:
            self.print_error(f"Erro durante a captura: {str(e)}")
        
        input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
    
    def show_system_status(self):
        """Exibe status do sistema"""
        self.print_banner()
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                          STATUS DO SISTEMA                               ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Status dos módulos
        modules = [
            ("Google Maps Integration", "ONLINE", Fore.GREEN),
            ("Selenium WebDriver", "ONLINE", Fore.GREEN),
            ("Data Export System", "ONLINE", Fore.GREEN),
            ("Neural Navigation", "ONLINE", Fore.GREEN),
            ("Cyberpunk Interface", "ONLINE", Fore.GREEN)
        ]
        
        for module, status, color in modules:
            print(f"{Fore.CYAN}►{Style.RESET_ALL} {module:<30} {color}[{status}]{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}Sistema operacional e pronto para captura de leads!{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
    
    def run(self):
        """Loop principal da interface"""
        while self.running:
            self.print_banner()
            self.print_menu()
            
            choice = self.get_user_input("Selecione uma opção", "choice")
            
            if choice == "1":
                self.capture_leads_interface()
            elif choice == "2":
                self.print_info("Configurações avançadas em desenvolvimento...")
                input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
            elif choice == "3":
                self.show_system_status()
            elif choice == "4":
                self.print_info("Histórico de operações em desenvolvimento...")
                input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
            elif choice == "0":
                self.print_warning("Desconectando do sistema...")
                self.print_loading_animation("Finalizando processos", 2)
                self.print_success("Sistema desconectado com segurança!")
                self.running = False
            else:
                self.print_error("Opção inválida!")

def main():
    """Função principal"""
    try:
        terminal = CyberpunkTerminal()
        terminal.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[SISTEMA INTERROMPIDO]{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Desconexão de emergência ativada!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[ERRO CRÍTICO]{Style.RESET_ALL} {str(e)}")

if __name__ == "__main__":
    main()
