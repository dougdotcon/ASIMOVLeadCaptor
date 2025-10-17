# 🔥 ASIMOV LeadCaptor - WhatsApp Bot

**Sistema completo de automação WhatsApp com IA e envio em massa usando Baileys**

## ✨ Características Principais

- 🤖 **Chat com IA** - ChatGPT integrado para conversas inteligentes
- 🎨 **Geração de Imagens** - DALL-E para criar imagens a partir de texto
- 📨 **Envio em Massa** - Sistema completo de disparador de mensagens
- 🧠 **Mensagens Únicas** - IA gera variações automáticas para cada contato
- 📊 **Suporte Excel/CSV** - Carregamento fácil de listas de contatos
- ⚡ **Baileys** - Biblioteca confiável para WhatsApp Web API
- 🎯 **Integração LeadCaptor** - Funciona com o sistema de captura de leads

## 🚀 Configuração Inicial

### 1. Instalar Dependências

```bash
cd BASEBAILEYS
npm install
```

### 2. Configurar APIs

Edite o arquivo `key.json`:

```json
{
  "keyopenai": "sua-chave-openai-aqui",
  "openrouter_api_key": "sua-chave-openrouter-aqui",
  "openrouter_base_url": "https://openrouter.ai/api/v1",
  "default_model": "deepseek/deepseek-r1-0528:free",
  "message_temperature": 0.8,
  "max_message_tokens": 150,
  "default_delay_seconds": 5,
  "max_messages_per_hour": 60
}
```

### 3. Executar o Sistema

```bash
node index.js
```

### 4. Conectar WhatsApp

1. Será exibido um QR Code no terminal
2. Abra o WhatsApp no seu celular
3. Vá em **Menu** > **Aparelhos conectados** > **Conectar aparelho**
4. Escaneie o QR Code exibido
5. Aguarde a confirmação de conexão

## 📱 Comandos Disponíveis

### 🤖 IA & Automação
- `/menu` - Menu principal com todos os comandos
- `/ai [pergunta]` - Chat com ChatGPT
- `/img [descrição]` - Gerar imagens com DALL-E
- `/mass` - Acessar sistema de envio em massa

### 📊 Envio em Massa
- `/loadcontacts` - Carregar arquivo Excel/CSV
- `/sendmass` - Enviar mensagens em massa
- `/testeenvio [número] [mensagem]` - Testar envio
- `/stats` - Ver estatísticas de envio
- `/stop` - Parar envio em andamento

### ⚙️ Sistema
- `/config` - Ver configurações atuais
- `/sc` - Informações do código fonte
- `/help` - Menu de ajuda

## 📄 Formato de Arquivos de Contatos

### Excel (.xlsx)
```
| name                    | phone_number  | address              |
|------------------------|---------------|---------------------|
| Clínica Veterinária    | 11999887766   | Rua das Flores, 123 |
| Pet Shop Central       | 11888777655   | Av. Principal, 456   |
```

### CSV (.csv)
```csv
name,phone_number,address
"Clínica Veterinária","11999887766","Rua das Flores, 123"
"Pet Shop Central","11888777655","Av. Principal, 456"
```

## 🎯 Sistema de Mensagens Únicas

O sistema usa IA para criar variações automáticas de cada mensagem:

**Template que você escreve:**
```
Olá {name}, encontrei seu contato no Google Maps e gostaria de conversar sobre uma oportunidade.
```

**Variações automáticas geradas:**
- "Oi Clínica Veterinária! Vi vocês no Maps e tenho uma proposta interessante. Podemos conversar?"
- "Bom dia Pet Shop Central! Consegui o contato pelo Google e queria apresentar algo. Quando poderíamos bater um papo?"

## 🔧 Funcionalidades Avançadas

### Controle via WhatsApp
- Todos os comandos funcionam diretamente no WhatsApp
- Interface híbrida: WhatsApp + Terminal
- Estatísticas em tempo real
- Controle de parada de emergência

### Validação Automática
- Formatação automática de números brasileiros
- Validação de arquivos de contatos
- Verificação de APIs configuradas
- Relatórios detalhados de envio

### Segurança e Limites
- Delay configurável entre mensagens (mín. 5s)
- Limite de mensagens por hora
- Validação de números de telefone
- Logs detalhados de todas as operações

## 🛡️ Boas Práticas

### Limites Recomendados
- **Delay mínimo**: 5 segundos entre mensagens
- **Máximo diário**: Até 100 mensagens
- **Horário**: Evite envios após 20h e antes das 8h
- **Teste sempre**: Use `/testeenvio` primeiro

### Templates Eficazes
- Use `{name}` para personalização
- Máximo 2 linhas por mensagem
- Seja direto sobre o motivo do contato
- Termine com uma pergunta ou convite

## 🔄 Integração com LeadCaptor

Este sistema funciona perfeitamente com o ASIMOV LeadCaptor:

1. **Captura de Leads**: Use o sistema principal para capturar leads do Google Maps
2. **Carregamento Automático**: Os arquivos Excel gerados são automaticamente compatíveis
3. **Envio Inteligente**: Use a IA para criar mensagens únicas para cada lead
4. **Monitoramento**: Acompanhe estatísticas e resultados em tempo real

## 📞 Solução de Problemas

### QR Code não aparece
- Verifique se o Node.js está instalado: `node --version`
- Limpe a sessão: exclua a pasta `yusril`
- Execute novamente: `node index.js`

### Erro de API
- Verifique as chaves no arquivo `key.json`
- Confirme se tem créditos nas contas (OpenAI/OpenRouter)
- Use modelos gratuitos quando disponíveis

### Mensagens não enviando
- Confirme que o WhatsApp está conectado
- Verifique formato dos números: `11999887766`
- Teste com `/testeenvio` primeiro

## 🎉 Recursos Implementados

- ✅ Sistema de envio em massa completo
- ✅ Geração de mensagens únicas com IA
- ✅ Carregamento de arquivos Excel/CSV
- ✅ Interface híbrida WhatsApp + Terminal
- ✅ Estatísticas e relatórios detalhados
- ✅ Validação automática de contatos
- ✅ Controle de delay e limites
- ✅ Comandos via WhatsApp
- ✅ Integração com sistema LeadCaptor

## 📄 Licença

MIT License - Baseado no projeto original [Wa-OpenAI](https://github.com/Sansekai/Wa-OpenAI)

Adaptado e expandido para o **ASIMOV LeadCaptor**

---

**🔥 ASIMOV LeadCaptor - Automatize sua prospecção com inteligência!**
