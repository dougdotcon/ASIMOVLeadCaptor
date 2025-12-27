# AsimovLeadCaptor

![Logo do Projeto](logo.png)

**Um sistema completo de captura de leads e disparo de mensagens WhatsApp com interface cyberpunk.**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org) [![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org) [![WhatsApp](https://img.shields.io/badge/WhatsApp-Bot-25D366.svg)](https://whatsapp.com) [![AI](https://img.shields.io/badge/AI-Powered-purple.svg)](https://openrouter.ai) [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Visão Geral

O AsimovLeadCaptor é uma ferramenta de automação full-stack projetada para capturar leads do Google Maps e disparar mensagens personalizadas via WhatsApp. Ele utiliza IA para a geração de mensagens e conta com uma interface baseada em terminal para uma experiência de usuário única.

## 🚀 Início Rápido

### Pré-requisitos
- **Python 3.7+**
- **Node.js 18+**
- Uma conta **WhatsApp** válida
- Chaves de API para **Serviços de IA** (OpenRouter, DALL-E, etc.)

### Instalação e Execução

1. **Clonar o repositório:**
   bash
   git clone https://github.com/seuusuario/AsimovLeadCaptor.git
   cd AsimovLeadCaptor
   

2. **Instalar Dependências:**
   bash
   # Dependências Python
   pip install -r requirements.txt

   # Dependências Node.js
   npm install
   

3. **Configurar Ambiente:**
   Crie um arquivo `.env` ou edite `config.json` com suas chaves de API e configurações.

4. **Executar a Aplicação:**
   
   **Windows:**
   cmd
   start_asimov.bat
   
   
   **Linux/Mac:**
   bash
   python app.py
   

## 🎮 Uso

Ao iniciar o programa, você verá o menu principal:

1. **🚀 Sistema Completo:** Executa o Gerador de Leads e o Disparador WhatsApp simultaneamente.
2. **🎯 Apenas Gerador:** Extrai dados do Google Maps.
3. **📱 Apenas Disparador:** Gerencia o envio de mensagens e a sessão.
4. **⚙️ Configurações:** Configure chaves de API e verifique o status.

### Fluxo de Trabalho

1. Selecione **[1] Sistema Completo** ou **[2] Apenas Gerador**.
2. Insira os critérios de busca (Nicho, Localização).
3. O sistema fará o scraping do Google Maps e salvará os leads em um banco de dados/CSV.
4. Selecione **[3] Apenas Disparador**.
5. Conecte seu WhatsApp escaneando o QR Code.
6. Inicie a campanha para enviar mensagens geradas por IA aos seus leads.

## 🤖 Integração com IA

O sistema se integra com LLMs para:
- **Personalizar Mensagens:** Intros únicas para cada lead baseadas no tipo de negócio.
- **Gerar Contexto:** Analisar dados do lead para criar ganchos relevantes.
- **Geração de Imagens (Opcional):** Usar DALL-E para gerar imagens personalizadas.

## ⚙️ Configuração

Arquivos principais:
- `config.json`: Configurações gerais (timeouts, delays, caminhos).
- `.env`: Armazenamento seguro de chaves de API e tokens.

## 📊 Funcionalidades

- **Captura de Leads:**
  - Scraping do Google Maps com filtros.
  - Validação e limpeza de dados.
  - Exportação para Excel/CSV.

- **Automação WhatsApp:**
  - Suporte a múltiplas sessões.
  - Reconexão automática.
  - Painel de estatísticas em tempo real.

- **Interface:**
  - Estética Cyberpunk/Terminal.
  - Sistema de menu interativo.

## 🔒 Isenção de Responsabilidade

*Automatizar o uso do WhatsApp viola os Termos de Serviço da plataforma. Use esta ferramenta com responsabilidade e por sua própria conta e risco. Este projeto é destinado a fins educacionais.*

## 📄 Licença

Licença MIT. Consulte o arquivo `LICENSE` para detalhes.