# 🔥 ASIMOV LEADCAPTOR CYBERPUNK SYSTEM 🔥

## 🎯 Visão Geral

Sistema completo de captura de leads e disparador de mensagens WhatsApp com interface cyberpunk. Combina web scraping do Google Maps com automação de mensagens via Baileys, tudo integrado em uma interface terminal futurística.

## ✨ Características Principais

### 🎨 Interface Cyberpunk
- **Banner ASCII animado** com arte cyberpunk
- **Cores neon** (ciano, verde, amarelo, magenta)
- **Animações de carregamento** com caracteres especiais
- **Menus estilizados** com bordas ASCII
- **Feedback visual** para todas as operações

### 🚀 Funcionalidades Completas
- **Captura de leads** do Google Maps
- **🔥 Sistema WhatsApp** com Baileys integrado
- **📱 Login via QR Code** - conecta com sua conta
- **🤖 Mensagens únicas** - IA gera variações automaticamente
- **Seleção de estados** brasileiros e americanos
- **Navegação contínua** com 4 fases de busca
- **Export automático** para Excel/CSV
- **Fluxo integrado** - captura ➜ mensagens automático

### 🆕 Novo Sistema de Mensagens WhatsApp
- **Baileys API** - conexão direta com WhatsApp
- **OpenRouter AI** - variações únicas de mensagens
- **Templates inteligentes** - nunca envia mensagem igual
- **Controle de delay** - evita bloqueios
- **Suporte Excel/CSV** - carrega listas de contatos
- **Teste integrado** - valida antes de enviar em lote

## 🛠️ Instalação e Configuração

### 🚀 Instalação Completa (Recomendada)
```bash
# 1. Sistema completo com WhatsApp
python start_whatsapp_system.py
```
Este script irá:
- ✅ Verificar Node.js (instale se necessário)
- ✅ Instalar dependências Python e Node.js
- ✅ Configurar arquivo .env
- ✅ Configurar API OpenRouter
- ✅ Executar testes do sistema
- ✅ Iniciar interface cyberpunk

### 📱 Apenas Sistema Cyberpunk
```bash
# 2. Apenas captura de leads
python start_cyberpunk.py
```

### ⚙️ Instalação Manual
```bash
# Python dependencies
pip install colorama pyfiglet selenium pandas webdriver-manager openpyxl

# Node.js dependencies (para WhatsApp)
cd whatsapp_sender
npm install
```

## 🔑 Configuração Inicial

### 1. API OpenRouter (para mensagens únicas)
1. Acesse [OpenRouter.ai](https://openrouter.ai) 
2. Crie conta gratuita
3. Obtenha API key
4. Configure no arquivo `whatsapp_sender/.env`

### 2. WhatsApp Login
1. Execute o sistema
2. Escolha `[1] INICIAR WHATSAPP & QR CODE LOGIN`
3. Escaneie QR Code com seu WhatsApp
4. Aguarde confirmação de conexão

### 3. Pronto para usar!
Agora pode capturar leads e enviar mensagens automaticamente.

## 🎮 Como Usar

### 1. Inicialização
Execute o launcher:
```bash
python start_cyberpunk.py
```

### 2. Novo Menu Principal Integrado
```
╔═══════════════════════════════════════════════════════════════════════════╗
║                           MENU PRINCIPAL                                 ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ [1] ► INICIAR WHATSAPP & QR CODE LOGIN                                   ║
║ [2] ► CAPTURAR LEADS DO GOOGLE MAPS                                      ║
║ [3] ► DISPARAR MENSAGENS WHATSAPP                                        ║
║ [4] ► STATUS DO SISTEMA                                                  ║
║ [5] ► CONFIGURAÇÕES AVANÇADAS                                            ║
║ [0] ► DESCONECTAR DO SISTEMA                                             ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### 3. 🔄 Fluxo Completo Integrado

#### Passo 1: Conectar WhatsApp
1. Escolha **[1] INICIAR WHATSAPP & QR CODE LOGIN**
2. Escaneie QR Code com WhatsApp
3. Aguarde confirmação de conexão

#### Passo 2: Capturar Leads
1. Escolha **[2] CAPTURAR LEADS DO GOOGLE MAPS**
2. Selecione **país** (Brasil/Estados Unidos)
3. Escolha o **estado** da lista
4. Digite o **bairro/cidade**
5. Digite a **palavra-chave** (ex: restaurante, dentista)
6. Digite a **quantidade** de leads desejada
7. Confirme a operação
8. **NOVO**: Pergunta se deseja abrir sistema de mensagens

#### Passo 3: Disparar Mensagens (Automático)
1. Escolha **[3] DISPARAR MENSAGENS WHATSAPP** ou aceite após captura
2. Sistema detecta último arquivo automaticamente
3. Configure template de mensagem
4. Defina delay entre envios (recomendado: 5-10s)
5. Inicie o disparo!

### 4. 🎯 Exemplo Completo de Uso
```
1. Conectar WhatsApp → QR Code → ✅ Conectado
2. Capturar leads:
   - País: Brasil
   - Estado: São Paulo  
   - Bairro: Vila Madalena
   - Palavra-chave: restaurante
   - Quantidade: 100
   - ✅ 100 leads capturados

3. Disparar mensagens:
   - Template: "Olá {name}! Vi vocês no Google Maps..."
   - Delay: 7 segundos
   - ✅ Mensagens enviadas com variações únicas!
```

## 🤖 Mensagens Inteligentes com IA

### Como Funciona a Variação Automática

**Seu template:**
```
Olá, poderia falar com {name}? Encontrei o contato no Google Maps e gostaria de agendar uma conversa.
```

**Variações geradas automaticamente:**
1. "Oi! Estou tentando entrar em contato com o {name}. Vi vocês no Google e queria conversar sobre algo interessante."
2. "Bom dia! Consegui o contato de vocês pelo Maps e gostaria de apresentar uma proposta. Podemos bater um papo?"
3. "Olá {name}! Vi o perfil de vocês online e tenho algo que pode interessar. Quando poderíamos conversar?"

### 🎯 Vantagens das Mensagens Únicas
- **Nunca repete** - cada mensagem é única
- **Mantém o propósito** - objetivo sempre claro
- **Natural e humana** - não parece robô
- **Evita bloqueios** - WhatsApp não detecta spam
- **Personalizada** - sempre usa o nome do contato

### ⚙️ Configurações Inteligentes
- **Temperatura**: 0.8 (criatividade balanceada)
- **Modelo**: DeepSeek R1 (gratuito)
- **Tokens**: 150 máximo por mensagem
- **Delay**: 5-10 segundos entre envios

## 🎨 Elementos Visuais

### Banner Principal
```
    ██████╗ ██████╗  ██████╗ ███████╗██████╗ ███████╗ ██████╗████████╗ ██████╗ 
    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔═══██╗
    ██████╔╝██████╔╝██║   ██║███████╗██████╔╝█████╗  ██║        ██║   ██║   ██║
    ██╔═══╝ ██╔══██╗██║   ██║╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██║   ██║
    ██║     ██║  ██║╚██████╔╝███████║██║     ███████╗╚██████╗   ██║   ╚██████╔╝
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ 
```

### Animações de Carregamento
```
[▓▓▓] Inicializando sistema neural [▓▓▓]
[▒▒▒] Conectando ao Google Maps [▒▒▒]
[░░░] Configurando parâmetros [░░░]
```

### Feedback de Status
```
[✓ SUCESSO] Operação concluída!
[✗ ERRO] Falha na conexão
[⚠ AVISO] Verificar parâmetros
[ℹ INFO] Sistema online
```

## 🔧 Arquitetura

### Arquivos Principais
- `cyberpunk_terminal.py` - Interface principal
- `start_cyberpunk.py` - Launcher com auto-instalação
- `google_maps_integration.py` - Backend de scraping
- `ui.py` - Constantes e dados (estados brasileiros)

### Dependências
- `colorama` - Cores no terminal
- `pyfiglet` - Arte ASCII
- `selenium` - Automação web
- `pandas` - Manipulação de dados
- `webdriver-manager` - Gerenciamento do ChromeDriver
- `openpyxl` - Export para Excel

## 🚀 Funcionalidades Avançadas

### Sistema de Navegação em 4 Fases
1. **Navegação Espiral** - Padrão sistemático
2. **Navegação Estendida** - Com zoom dinâmico
3. **Navegação Aleatória** - Movimentos inteligentes
4. **Sistema de Reset** - Mudança automática de área

### Capacidades de Captura
- **Até 1000+ leads** por operação
- **Navegação contínua** sem limites
- **Detecção automática** de áreas vazias
- **Reset inteligente** para novas regiões

## 🎯 Vantagens da Interface Terminal

### Performance
- **Menor uso de memória** (sem GUI)
- **Execução mais rápida** 
- **Compatibilidade universal** (qualquer terminal)

### Experiência
- **Visual cyberpunk único**
- **Feedback em tempo real**
- **Operação simplificada**
- **Estilo futurístico**

### Flexibilidade
- **Execução remota** via SSH
- **Automação fácil** via scripts
- **Logs detalhados** no terminal
- **Controle total** via teclado

## 🔥 Comandos Rápidos

### Iniciar Sistema
```bash
python start_cyberpunk.py
```

### Captura Rápida (exemplo)
1. Execute o sistema
2. Digite `1` (Iniciar Captura)
3. Selecione estado (ex: `25` para São Paulo)
4. Digite bairro (ex: `Copacabana`)
5. Digite palavra-chave (ex: `restaurante`)
6. Digite quantidade (ex: `200`)
7. Digite `s` para confirmar

### Verificar Status
1. Execute o sistema
2. Digite `3` (Status do Sistema)

## 🎨 Personalização

A interface pode ser facilmente personalizada modificando:
- **Cores** no arquivo `cyberpunk_terminal.py`
- **Arte ASCII** nos banners
- **Animações** de carregamento
- **Mensagens** de status

## 🚀 Próximas Funcionalidades

- [ ] Histórico de operações
- [ ] Configurações avançadas
- [ ] Export para múltiplos formatos
- [ ] Agendamento de capturas
- [ ] Dashboard de estatísticas
- [ ] Integração com APIs

## 🎯 Conclusão

A interface cyberpunk oferece uma experiência única e moderna para captura de leads, mantendo toda a funcionalidade do sistema original com um visual futurístico e performance otimizada.

**Bem-vindo ao futuro da captura de leads! 🔥**
