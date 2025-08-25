# 🔥 PROSPECTOR CYBERPUNK TERMINAL 🔥

## 🎯 Visão Geral

Interface terminal cyberpunk ASCII para o sistema Prospector de captura de leads. Esta interface substitui completamente a GUI tradicional por uma experiência terminal futurística e estilizada.

## ✨ Características

### 🎨 Interface Cyberpunk
- **Banner ASCII animado** com arte cyberpunk
- **Cores neon** (ciano, verde, amarelo, magenta)
- **Animações de carregamento** com caracteres especiais
- **Menus estilizados** com bordas ASCII
- **Feedback visual** para todas as operações

### 🚀 Funcionalidades
- **Captura de leads** do Google Maps
- **Seleção de estados** brasileiros
- **Configuração de parâmetros** (bairro, palavra-chave, quantidade)
- **Status do sistema** em tempo real
- **Navegação contínua** com 4 fases de busca
- **Export automático** para Excel/CSV

## 🛠️ Instalação

### 1. Método Automático (Recomendado)
```bash
python start_cyberpunk.py
```
O script irá verificar e instalar automaticamente todas as dependências necessárias.

### 2. Método Manual
```bash
pip install colorama pyfiglet selenium pandas webdriver-manager openpyxl
python cyberpunk_terminal.py
```

## 🎮 Como Usar

### 1. Inicialização
Execute o launcher:
```bash
python start_cyberpunk.py
```

### 2. Menu Principal
```
╔═══════════════════════════════════════════════════════════════════════════╗
║                           MENU PRINCIPAL                                 ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ [1] ► INICIAR CAPTURA DE LEADS                                           ║
║ [2] ► CONFIGURAÇÕES AVANÇADAS                                            ║
║ [3] ► STATUS DO SISTEMA                                                  ║
║ [4] ► HISTÓRICO DE OPERAÇÕES                                             ║
║ [0] ► DESCONECTAR DO SISTEMA                                             ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### 3. Captura de Leads
1. Selecione **[1] INICIAR CAPTURA DE LEADS**
2. Escolha o **estado** da lista
3. Digite o **bairro/cidade**
4. Digite a **palavra-chave** (ex: restaurante, dentista)
5. Digite a **quantidade** de leads desejada
6. Confirme a operação

### 4. Exemplo de Uso
```
Estado: São Paulo
Bairro/Cidade: Vila Madalena
Palavra-chave: restaurante
Quantidade: 100
```

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
