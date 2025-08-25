"""
Integração do Google Maps para o PROSPECTO.
Sistema de captura de leads e automação de mensagens.
Versão com navegação contínua implementada.
"""
from dataclasses import dataclass, asdict, field
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
import os
import random
from datetime import datetime
from tqdm import tqdm

@dataclass
class Business:
    """Representa um negócio extraído do Google Maps."""
    nome: str = "Nome não disponível"
    endereco: str = "Endereço não disponível"
    telefone: str = "Telefone não disponível"
    site: str = "Site não disponível"
    categoria: str = "Categoria não disponível"
    horario: str = "Horário não disponível"
    avaliacao: str = "Avaliação não disponível"
    total_avaliacoes: str = "Total de avaliações não disponível"
    latitude: str = "Latitude não disponível"
    longitude: str = "Longitude não disponível"
    email: str = "Email não disponível"
    whatsapp: str = "WhatsApp não disponível"
    instagram: str = "Instagram não disponível"
    facebook: str = "Facebook não disponível"
    descricao: str = "Descrição não disponível"
    preco: str = "Preço não disponível"
    preco: str = "Preço não disponível"
    descricao: str = "Descrição não disponível"
    fotos: list = field(default_factory=list)

@dataclass
class BusinessList:
    """Armazena uma lista de objetos Business e permite salvar os resultados em Excel ou CSV."""
    business_list: list[Business] = field(default_factory=list)

    def dataframe(self):
        """Transforma a lista de negócios em um DataFrame do pandas."""
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="_")

    def save_to_excel(self, filename, save_dir):
        """Salva o DataFrame em um arquivo Excel."""
        try:
            if not save_dir:
                return "Diretório não especificado"

            # Criar diretório se não existir
            os.makedirs(save_dir, exist_ok=True)

            # Verificar se há dados para salvar
            if not self.business_list:
                return "Nenhum dado para salvar"

            full_path = f'{save_dir}/{filename}.xlsx'
            df = self.dataframe()

            # Verificar se o DataFrame não está vazio
            if df.empty:
                return "DataFrame vazio - nenhum dado para salvar"

            df.to_excel(full_path, index=False)
            return f"Arquivo Excel salvo em: {full_path} ({len(self.business_list)} leads)"

        except Exception as e:
            return f"Erro ao salvar arquivo Excel: {str(e)}"

    def save_to_csv(self, filename, save_dir):
        """Salva o DataFrame em um arquivo CSV."""
        try:
            if not save_dir:
                return "Diretório não especificado"

            # Criar diretório se não existir
            os.makedirs(save_dir, exist_ok=True)

            # Verificar se há dados para salvar
            if not self.business_list:
                return "Nenhum dado para salvar"

            full_path = f'{save_dir}/{filename}.csv'
            df = self.dataframe()

            # Verificar se o DataFrame não está vazio
            if df.empty:
                return "DataFrame vazio - nenhum dado para salvar"

            df.to_csv(full_path, index=False, sep=';', encoding='utf-8-sig')
            return f"Arquivo CSV salvo em: {full_path} ({len(self.business_list)} leads)"

        except Exception as e:
            return f"Erro ao salvar arquivo CSV: {str(e)}"

def move_map(navegador, direction='right', distance=10):
    """
    Move o mapa na direção especificada com suporte a zoom e distâncias variáveis.
    direction: 'right', 'left', 'up', 'down', 'zoom_in', 'zoom_out'
    distance: número de movimentos (padrão: 10)
    """
    # Primeiro clica no mapa para garantir que está focado
    map_element = navegador.find_element(By.CLASS_NAME, 'widget-scene')
    action = ActionChains(navegador)
    action.move_to_element(map_element).click().perform()
    time.sleep(1)

    # Suporte a zoom
    if direction == 'zoom_out':
        # Zoom out usando Ctrl + -
        for _ in range(distance):
            action.key_down(Keys.CONTROL).send_keys('-').key_up(Keys.CONTROL).perform()
            time.sleep(0.2)
        time.sleep(4)  # Aguarda o zoom carregar
        return
    elif direction == 'zoom_in':
        # Zoom in usando Ctrl + +
        for _ in range(distance):
            action.key_down(Keys.CONTROL).send_keys('+').key_up(Keys.CONTROL).perform()
            time.sleep(0.2)
        time.sleep(4)  # Aguarda o zoom carregar
        return

    # Mapeia a direção para a tecla correspondente
    key_map = {
        'right': Keys.ARROW_RIGHT,
        'left': Keys.ARROW_LEFT,
        'up': Keys.ARROW_UP,
        'down': Keys.ARROW_DOWN
    }

    # Pressiona a tecla várias vezes para mover o mapa
    key = key_map.get(direction, Keys.ARROW_RIGHT)
    for _ in range(distance):
        action.send_keys(key).perform()
        time.sleep(0.1)

    # Aguarda um pouco para o mapa carregar (tempo aumentado)
    time.sleep(4)

def get_spiral_navigation_pattern(max_radius=15):
    """
    Gera um padrão de navegação espiral expandido para cobertura máxima.
    max_radius: raio máximo da espiral (padrão: 15, antes era 8)
    """
    pattern = []

    # Movimento inicial para o centro
    pattern.append(('right', 1))

    # Gerar espiral expandida
    for radius in range(1, max_radius + 1):
        # Movimentos horizontais e verticais
        for direction, distance in [
            ('up', radius), ('left', radius), ('down', radius), ('right', radius),
            ('up', radius), ('right', radius), ('down', radius), ('left', radius)
        ]:
            pattern.append((direction, distance * 2))  # Distância dobrada para maior cobertura

        # Movimentos diagonais simulados (combinação de direções)
        if radius % 2 == 0:  # A cada 2 raios, adicionar movimentos diagonais
            pattern.extend([
                ('up', radius), ('right', radius),    # Diagonal superior direita
                ('down', radius), ('right', radius),  # Diagonal inferior direita
                ('down', radius), ('left', radius),   # Diagonal inferior esquerda
                ('up', radius), ('left', radius)      # Diagonal superior esquerda
            ])

    return pattern

def get_extended_navigation_pattern():
    """
    Gera um padrão de navegação estendida com zoom para cobertura de áreas maiores.
    """
    pattern = []

    # Fase 1: Zoom out para ver área maior
    pattern.extend([
        ('zoom_out', 3),
        ('right', 50), ('down', 50), ('left', 100), ('up', 100),
        ('right', 50), ('zoom_in', 2)
    ])

    # Fase 2: Navegação por quadrantes
    quadrants = [
        [('right', 30), ('up', 30)],      # Quadrante superior direito
        [('left', 60), ('up', 30)],       # Quadrante superior esquerdo
        [('left', 30), ('down', 60)],     # Quadrante inferior esquerdo
        [('right', 60), ('down', 30)]     # Quadrante inferior direito
    ]

    for quadrant in quadrants:
        pattern.extend(quadrant)
        pattern.append(('zoom_out', 1))
        pattern.append(('zoom_in', 1))

    return pattern

def reset_search_in_new_area(navegador, search_term, callback=None):
    """
    Reseta a busca em uma nova área distante.
    """
    try:
        if callback:
            callback("[RESET] Movendo para área distante...")

        # Move para uma área bem distante
        move_map(navegador, 'right', 50)
        move_map(navegador, 'down', 50)
        time.sleep(3)

        # Limpa a busca atual
        search_box = navegador.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        search_box.clear()
        time.sleep(2)

        # Refaz a busca
        search_box.send_keys(search_term)
        time.sleep(1)
        navegador.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').click()
        time.sleep(10)

        if callback:
            callback("[RESET] Busca resetada com sucesso!")

        return True
    except Exception as e:
        if callback:
            callback(f"[ERRO] Falha no reset: {str(e)}")
        return False

def main_query(search_for, total, location, save_dir, file_format, headless_mode=True, callback=None):
    """
    Executa a consulta no Google Maps e extrai os dados dos estabelecimentos.

    Parâmetros:
      search_for: termo de busca (ex.: "restaurante Rio de Janeiro")
      total: número de resultados desejados
      location: localização para refinar a consulta
      save_dir: diretório onde os resultados serão salvos
      file_format: "excel" ou "csv"
      headless_mode: se True, executa o navegador em modo headless (invisível)
      callback: função opcional para receber atualizações de status
    """
    # Configura o Chrome
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")  # Desativa aceleração por hardware
    chrome_options.add_argument("--enable-unsafe-swiftshader")  # Permite SwiftShader

    # Suprimir mensagens de erro e logs desnecessários
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    # chrome_options.add_argument("--disable-javascript")  # REMOVIDO - Google Maps precisa de JS
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-software-rasterizer")  # Evita problemas com renderização

    # Adiciona modo headless se solicitado
    if headless_mode:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Suprimir logs do ChromeDriverManager e WebDriver
    import os
    import logging
    os.environ['WDM_LOG_LEVEL'] = '0'
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    if callback:
        callback("[INFO] Abrindo Google Maps...")
    navegador.get("https://www.google.com.br/maps")
    time.sleep(3)

    # Insere a localização e executa a busca inicial
    if callback:
        callback(f"[INFO] Buscando localização: {location}...")
    navegador.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys(location)
    time.sleep(2)
    navegador.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').click()
    time.sleep(15)
    navegador.find_element(By.XPATH, '//*[@id="searchbox"]/div[2]/button').click()
    time.sleep(5)

    # Realiza a busca do termo combinado (negócio + localização)
    if callback:
        callback(f"[INFO] Buscando termo: {search_for}...")
    navegador.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys(search_for)
    navegador.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').click()
    time.sleep(10)

    business_list = BusinessList()
    i = 0

    # ✅ NAVEGAÇÃO CONTÍNUA IMPLEMENTADA - SISTEMA EM 4 FASES
    # Padrões de navegação
    spiral_pattern = get_spiral_navigation_pattern(max_radius=15)  # Raio expandido
    extended_pattern = get_extended_navigation_pattern()

    # Limites muito mais generosos
    max_empty_areas = 8  # Antes era 3
    max_reset_attempts = 5
    max_navigation_attempts = len(spiral_pattern) + len(extended_pattern) + 50

    # Contadores
    navigation_attempts = 0
    areas_without_results = 0
    reset_attempts = 0
    pattern_index = 0
    current_phase = "ESPIRAL"  # ESPIRAL -> ESTENDIDA -> ALEATÓRIA -> RESET

    # Timeout para evitar travamentos
    start_time = time.time()
    max_execution_time = 300  # 5 minutos máximo

    if callback:
        callback(f"[NAVEGAÇÃO CONTÍNUA] Iniciando busca com sistema em 4 fases")
        callback(f"[INFO] Meta: {total} empresas | Padrão espiral: {len(spiral_pattern)} movimentos | Padrão estendido: {len(extended_pattern)} movimentos")

    # Primeira verificação: tentar extrair leads da página atual antes de navegar
    if callback:
        callback(f"[INFO] Verificando leads na página inicial...")

    # Aguardar a página carregar completamente
    time.sleep(5)

    while i < total and navigation_attempts < max_navigation_attempts and reset_attempts < max_reset_attempts:
        # Verificar timeout para evitar travamentos
        elapsed_time = time.time() - start_time
        if elapsed_time > max_execution_time:
            if callback:
                callback(f"[TIMEOUT] Operação interrompida após {elapsed_time:.1f} segundos para evitar travamento.")
            break
        previously_counted = 0
        stuck_count = 0

        try:
            # Verificar se já atingiu a meta antes de fazer scroll/navegação
            list_elem = navegador.find_elements(By.CLASS_NAME, 'hfpxzc')
            if callback:
                callback(f"[DEBUG] Encontrados {len(list_elem)} elementos na página atual.")

            if len(list_elem) >= total:
                if callback:
                    callback(f"[SUCESSO] Encontrados {len(list_elem)} elementos na página. Meta de {total} pode ser atingida!")
                # Não fazer break aqui - continuar para processar os elementos
            elif len(list_elem) == 0:
                if callback:
                    callback(f"[AVISO] Nenhum elemento encontrado. Aguardando página carregar...")
                time.sleep(10)
                continue
        except Exception as e:
            if callback:
                callback(f"[ERRO] Erro ao verificar elementos: {str(e)}")
            time.sleep(5)
            continue

        # Se já há elementos suficientes, pular scroll e ir direto para processamento
        list_elem = navegador.find_elements(By.CLASS_NAME, 'hfpxzc')
        if len(list_elem) >= total:
            if callback:
                callback(f"[INFO] Elementos suficientes encontrados ({len(list_elem)}). Pulando scroll.")
        else:
            # Fazer scroll apenas se não há elementos suficientes
            scroll_attempts = 0
            max_scroll_attempts = 10
            while True:
                # Verificar timeout no scroll
                if time.time() - start_time > max_execution_time:
                    if callback:
                        callback(f"[TIMEOUT] Scroll interrompido por timeout.")
                    break

                scroll_attempts += 1
                if scroll_attempts > max_scroll_attempts:
                    if callback:
                        callback(f"[AVISO] Máximo de tentativas de scroll atingido ({max_scroll_attempts}).")
                    break

                list_elem = navegador.find_elements(By.CLASS_NAME, 'hfpxzc')
                if not list_elem:
                    if callback:
                        callback(f"[AVISO] Nenhum elemento encontrado na tentativa {scroll_attempts}. Tentando novamente...")
                    time.sleep(5)
                    if scroll_attempts >= 3:  # Após 3 tentativas sem elementos, sair
                        if callback:
                            callback("[ERRO] Nenhum elemento encontrado após múltiplas tentativas.")
                        break  # Sair do loop, mas continuar para salvar arquivo
                    continue

                action = ActionChains(navegador)
                try:
                    action.move_to_element(list_elem[-1]).perform()
                except Exception:
                    list_elem = navegador.find_elements(By.CLASS_NAME, 'hfpxzc')
                    action.move_to_element(list_elem[-1]).perform()
                time.sleep(5)

                scroll_origin = ScrollOrigin.from_element(list_elem[-1])
                action.scroll_from_origin(scroll_origin, 0, 1200).perform()
                time.sleep(20)
                action.scroll_from_origin(scroll_origin, 0, 250).perform()

                current_count = len(list_elem)
                if current_count == previously_counted:
                    stuck_count += 1
                    if stuck_count >= 3:  # Se ficar preso 3 vezes, consideramos que chegamos ao limite
                        break
                else:
                    stuck_count = 0
                    previously_counted = current_count

        # Processa os elementos encontrados
        list_elem = navegador.find_elements(By.CLASS_NAME, 'hfpxzc')
        if callback:
            callback(f"[DEBUG] Encontrados {len(list_elem)} elementos na página. Processando a partir do índice {i}")

        # Criar barra de progresso
        elementos_para_processar = list_elem[i:total] if len(list_elem) >= total else list_elem[i:]
        if callback:
            callback(f"[INFO] Iniciando processamento de {len(elementos_para_processar)} elementos...")

        # Usar tqdm para barra de progresso
        progress_bar = tqdm(
            elementos_para_processar,
            desc="🔍 Extraindo leads",
            unit="lead",
            initial=i,
            total=total,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} leads [{elapsed}<{remaining}]"
        )

        for element in progress_bar:
            if i >= total:
                if callback:
                    callback(f"[SUCESSO] Meta atingida! {i} leads capturados de {total} solicitados.")
                break

            try:
                time.sleep(2)
                navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(2)
                try:
                    element.click()
                except Exception as click_err:
                    error_msg = f"[ERRO] Falha ao clicar no elemento {i}: {str(click_err)}"
                    if callback:
                        callback(error_msg)
                    print(error_msg)
                    i += 1
                    continue
                time.sleep(6)

                # XPaths para extração dos dados
                name_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1'
                address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'

                # Extrai os dados
                business = Business()

                try:
                    business.nome = navegador.find_element(By.XPATH, name_xpath).text
                except NoSuchElementException:
                    business.nome = f"Nome não disponível {i}"

                try:
                    business.endereco = navegador.find_element(By.XPATH, address_xpath).text
                except NoSuchElementException:
                    business.endereco = "Endereço não disponível"

                try:
                    business.site = navegador.find_element(By.XPATH, website_xpath).text
                except NoSuchElementException:
                    business.site = "Site não disponível"

                try:
                    business.telefone = navegador.find_element(By.XPATH, phone_number_xpath).text
                except NoSuchElementException:
                    business.telefone = "Telefone não disponível"

                # Extrair categoria/tipo de negócio
                try:
                    # Tentar diferentes XPaths para categoria
                    categoria_xpaths = [
                        '//button[@jsaction="pane.rating.category"]//span',
                        '//div[contains(@class, "fontBodyMedium") and contains(text(), "·")]',
                        '//span[contains(@class, "DkEaL")]',
                        '//div[@data-value="Category"]//span'
                    ]
                    for xpath in categoria_xpaths:
                        try:
                            business.categoria = navegador.find_element(By.XPATH, xpath).text
                            break
                        except NoSuchElementException:
                            continue
                    else:
                        business.categoria = "Categoria não disponível"
                except Exception:
                    business.categoria = "Categoria não disponível"

                # Extrair avaliação
                try:
                    # Tentar diferentes XPaths para avaliação
                    avaliacao_xpaths = [
                        '//span[@aria-hidden="true" and contains(text(), ",")]',
                        '//div[contains(@class, "F7nice")]//span[@aria-hidden="true"]',
                        '//span[contains(text(), "4,") or contains(text(), "3,") or contains(text(), "5,")]'
                    ]
                    for xpath in avaliacao_xpaths:
                        try:
                            business.avaliacao = navegador.find_element(By.XPATH, xpath).text
                            break
                        except NoSuchElementException:
                            continue
                    else:
                        business.avaliacao = "Avaliação não disponível"
                except Exception:
                    business.avaliacao = "Avaliação não disponível"

                # Extrair total de avaliações
                try:
                    # Tentar diferentes XPaths para total de avaliações
                    total_avaliacoes_xpaths = [
                        '//span[contains(text(), "avaliações") or contains(text(), "reviews")]',
                        '//button[@jsaction="pane.rating.moreReviews"]//span[contains(text(), "(")]',
                        '//div[contains(@class, "F7nice")]//span[contains(text(), "(")]'
                    ]
                    for xpath in total_avaliacoes_xpaths:
                        try:
                            business.total_avaliacoes = navegador.find_element(By.XPATH, xpath).text
                            break
                        except NoSuchElementException:
                            continue
                    else:
                        business.total_avaliacoes = "Total de avaliações não disponível"
                except Exception:
                    business.total_avaliacoes = "Total de avaliações não disponível"

                # Extrair horário de funcionamento
                try:
                    horario_xpath = '//div[contains(@class, "t39EBf")]//div[contains(@class, "fontBodyMedium")]'
                    business.horario = navegador.find_element(By.XPATH, horario_xpath).text
                except NoSuchElementException:
                    business.horario = "Horário não disponível"

                # Extrair WhatsApp (se disponível)
                try:
                    whatsapp_xpath = '//a[contains(@href, "wa.me") or contains(@href, "whatsapp")]'
                    whatsapp_element = navegador.find_element(By.XPATH, whatsapp_xpath)
                    business.whatsapp = whatsapp_element.get_attribute("href")
                except NoSuchElementException:
                    business.whatsapp = "WhatsApp não disponível"

                # Extrair Instagram (se disponível)
                try:
                    instagram_xpath = '//a[contains(@href, "instagram.com")]'
                    instagram_element = navegador.find_element(By.XPATH, instagram_xpath)
                    business.instagram = instagram_element.get_attribute("href")
                except NoSuchElementException:
                    business.instagram = "Instagram não disponível"

                # Extrair Facebook (se disponível)
                try:
                    facebook_xpath = '//a[contains(@href, "facebook.com")]'
                    facebook_element = navegador.find_element(By.XPATH, facebook_xpath)
                    business.facebook = facebook_element.get_attribute("href")
                except NoSuchElementException:
                    business.facebook = "Facebook não disponível"

                # Adiciona o negócio à lista
                business_list.business_list.append(business)
                time.sleep(3)
                i += 1

                # Atualizar barra de progresso
                progress_bar.set_description(f"🔍 Extraindo leads - {business.nome[:30]}...")
                progress_bar.update(1)

                if callback:
                    porcentagem = (i / total) * 100
                    callback(f"[PROGRESSO] Lead {i}/{total} extraído: {business.nome}")

                # Verificar se já atingiu a meta
                if i >= total:
                    progress_bar.close()
                    if callback:
                        callback(f"[SUCESSO] Meta atingida! {i} leads capturados com sucesso!")
                    break  # Sair do loop, mas não retornar ainda (precisa salvar arquivo)

            except StaleElementReferenceException:
                error_msg = f"[AVISO] Elemento {i} está desatualizado, tentando próximo registro..."
                if callback:
                    callback(error_msg)
                print(error_msg)
                i += 1
                continue

        # ✅ SISTEMA DE NAVEGAÇÃO CONTÍNUA EM 4 FASES
        # Só navegar se ainda não atingiu a meta
        if i < total:
            initial_count = i

            if callback:
                callback(f"[INFO] Leads coletados: {i}/{total}. Continuando navegação...")

            # Verificar se não há progresso há muito tempo
            if i == 0 and navigation_attempts > 10:
                if callback:
                    callback(f"[AVISO] Nenhum lead encontrado após {navigation_attempts} tentativas. Pode não haver resultados para esta busca.")
                break

            # FASE 1: NAVEGAÇÃO ESPIRAL EXPANDIDA
            if current_phase == "ESPIRAL" and pattern_index < len(spiral_pattern):
                direction, distance = spiral_pattern[pattern_index]
                if callback:
                    callback(f"[NAVEGAÇÃO ESPIRAL] Movendo mapa para {direction} (distância: {distance}) - Tentativa {pattern_index + 1}/{len(spiral_pattern)}")
                move_map(navegador, direction, distance)
                pattern_index += 1
                navigation_attempts += 1
                time.sleep(10)  # Aguarda o mapa carregar

                # Se terminou a navegação espiral, muda para fase estendida
                if pattern_index >= len(spiral_pattern):
                    current_phase = "ESTENDIDA"
                    pattern_index = 0
                    if callback:
                        callback(f"[FASE CONCLUÍDA] Navegação espiral finalizada. Iniciando navegação estendida...")

            # FASE 2: NAVEGAÇÃO ESTENDIDA COM ZOOM
            elif current_phase == "ESTENDIDA" and pattern_index < len(extended_pattern):
                direction, distance = extended_pattern[pattern_index]
                if callback:
                    callback(f"[NAVEGAÇÃO ESTENDIDA] Movendo mapa para {direction} (distância: {distance}) - Tentativa {pattern_index + 1}/{len(extended_pattern)}")
                move_map(navegador, direction, distance)
                pattern_index += 1
                navigation_attempts += 1
                time.sleep(10)  # Aguarda o mapa carregar

                # Se terminou a navegação estendida, muda para fase aleatória
                if pattern_index >= len(extended_pattern):
                    current_phase = "ALEATÓRIA"
                    if callback:
                        callback(f"[FASE CONCLUÍDA] Navegação estendida finalizada. Iniciando navegação aleatória...")

            # FASE 3: NAVEGAÇÃO ALEATÓRIA INTELIGENTE
            elif current_phase == "ALEATÓRIA" and navigation_attempts < max_navigation_attempts:
                # Movimentos aleatórios com distâncias maiores
                directions = ['right', 'left', 'up', 'down', 'zoom_out', 'zoom_in']
                direction = random.choice(directions)

                if direction in ['zoom_out', 'zoom_in']:
                    distance = random.randint(1, 3)
                else:
                    distance = random.randint(20, 40)  # Distâncias maiores

                if callback:
                    callback(f"[NAVEGAÇÃO ALEATÓRIA] Movendo mapa para {direction} (distância: {distance})")
                move_map(navegador, direction, distance)
                navigation_attempts += 1
                time.sleep(10)  # Aguarda o mapa carregar

                # Se esgotou tentativas de navegação, muda para fase de reset
                if navigation_attempts >= max_navigation_attempts:
                    current_phase = "RESET"
                    if callback:
                        callback(f"[FASE CONCLUÍDA] Navegação aleatória finalizada. Iniciando sistema de reset...")

            # FASE 4: SISTEMA DE RESET AUTOMÁTICO
            elif current_phase == "RESET" and reset_attempts < max_reset_attempts:
                if callback:
                    callback(f"[RESET] Tentando resetar busca em nova área (tentativa {reset_attempts + 1}/{max_reset_attempts})")

                if reset_search_in_new_area(navegador, search_for, callback):
                    reset_attempts += 1
                    navigation_attempts = 0  # Reinicia contador de navegação
                    current_phase = "ESPIRAL"  # Volta para fase espiral
                    pattern_index = 0
                    areas_without_results = 0  # Reinicia contador de áreas vazias
                    time.sleep(10)
                else:
                    break  # Se falhou no reset, para a busca

            else:
                # Se esgotou todas as fases e tentativas
                if callback:
                    callback(f"[FINALIZAÇÃO] Todas as estratégias de navegação foram esgotadas.")
                    callback(f"[ESTATÍSTICAS] Tentativas de navegação: {navigation_attempts}")
                    callback(f"[ESTATÍSTICAS] Tentativas de reset: {reset_attempts}")
                    callback(f"[ESTATÍSTICAS] Áreas sem resultados: {areas_without_results}")
                break

            # Verifica se encontrou novos resultados nesta área
            if i > initial_count:
                areas_without_results = 0  # Reinicia contador se encontrou resultados
                if callback:
                    callback(f"[SUCESSO] Encontrados {i - initial_count} novos resultados nesta área!")
            else:
                areas_without_results += 1
                if callback:
                    callback(f"[AVISO] Nenhum resultado novo nesta área ({areas_without_results}/{max_empty_areas})")

                # Se muitas áreas sem resultados, acelera para próxima fase
                if areas_without_results >= max_empty_areas:
                    if current_phase == "ESPIRAL":
                        current_phase = "ESTENDIDA"
                        pattern_index = 0
                        if callback:
                            callback(f"[ACELERAÇÃO] Muitas áreas vazias. Pulando para navegação estendida...")
                    elif current_phase == "ESTENDIDA":
                        current_phase = "ALEATÓRIA"
                        if callback:
                            callback(f"[ACELERAÇÃO] Muitas áreas vazias. Pulando para navegação aleatória...")
                    elif current_phase == "ALEATÓRIA":
                        current_phase = "RESET"
                        if callback:
                            callback(f"[ACELERAÇÃO] Muitas áreas vazias. Pulando para sistema de reset...")

                    areas_without_results = 0  # Reinicia contador

    # ✅ ESTATÍSTICAS FINAIS DA NAVEGAÇÃO CONTÍNUA
    if callback:
        callback(f"[FINALIZAÇÃO] Extração concluída! Total de empresas encontradas: {i}")
        if i >= total:
            callback(f"[SUCESSO] Meta atingida! {i} empresas extraídas com sucesso.")
        else:
            callback(f"[AVISO] Meta não atingida. Encontradas {i} de {total} empresas solicitadas.")
        callback(f"[ESTATÍSTICAS] Tentativas de navegação: {navigation_attempts}")
        callback(f"[ESTATÍSTICAS] Tentativas de reset: {reset_attempts}")
        callback(f"[ESTATÍSTICAS] Áreas sem resultados: {areas_without_results}")

    # Finaliza a extração e salva automaticamente os dados
    updated_string = search_for.replace(" ", "_")
    save_result = None
    if file_format.lower() == "excel":
        save_result = business_list.save_to_excel(f'maps_data_{updated_string}', save_dir)
    elif file_format.lower() == "csv":
        save_result = business_list.save_to_csv(f'maps_data_{updated_string}', save_dir)
    else:
        save_result = "Formato de arquivo inválido."

    if callback:
        callback(save_result)

    # Fecha o navegador
    navegador.quit()

    # Retornar a lista de leads, não a mensagem de salvamento
    return business_list.business_list
