# 🔥 ASIMOV WhatsApp Sender

Sistema de disparador de mensagens WhatsApp integrado ao ASIMOV LeadCaptor usando Baileys.

## ✨ Características

- 📱 **Login via QR Code** - Conecta com sua conta WhatsApp pessoal
- 🤖 **Mensagens únicas** - Usa OpenRouter AI para criar variações automaticamente
- 📊 **Suporte Excel/CSV** - Carrega listas de contatos facilmente
- ⚡ **Baileys** - Biblioteca confiável para WhatsApp Web API
- 🎯 **Integração total** - Funciona perfeitamente com o sistema cyberpunk

## 🚀 Configuração Inicial

### 1. Configurar API OpenRouter

1. Crie uma conta no [OpenRouter](https://openrouter.ai)
2. Obtenha sua API key gratuita
3. Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

4. Edite o arquivo `.env` e adicione sua chave:

```bash
OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui
```

### 2. Primeiro Login no WhatsApp

Quando executar pela primeira vez:

1. Será exibido um QR Code no terminal
2. Abra o WhatsApp no seu celular
3. Vá em **Menu** > **Aparelhos conectados** > **Conectar aparelho**
4. Escaneie o QR Code exibido
5. Aguarde a confirmação de conexão

## 📋 Como Usar

### Via Sistema Principal (Recomendado)

1. Execute o terminal cyberpunk:
   ```bash
   python start_cyberpunk.py
   ```

2. **Passo 1**: Escolha opção `[1] ► INICIAR WHATSAPP & QR CODE LOGIN`
   - Escaneie o QR Code para conectar

3. **Passo 2**: Escolha opção `[2] ► CAPTURAR LEADS DO GOOGLE MAPS`
   - Configure sua busca normalmente
   - Após a captura, escolha "s" para abrir sistema de mensagens

4. **Passo 3**: No sistema de mensagens:
   - Opção `[1]` usa automaticamente o arquivo da última busca
   - Configure template de mensagem
   - Defina delay entre envios
   - Inicie o disparo!

### Uso Manual

```bash
cd whatsapp_sender
node whatsapp_sender.js
```

## 🎯 Templates de Mensagem Inteligentes

O sistema usa IA para criar variações únicas de cada mensagem:

**Template que você escreve:**
```
Olá, poderia falar com {name}? Encontrei o contato no Google Maps e gostaria de agendar uma conversa.
```

**Variações automáticas geradas:**
- "Oi! Estou tentando entrar em contato com o {name}. Vi vocês no Google e queria conversar sobre algo interessante."
- "Bom dia! Consegui o contato de vocês pelo Maps e gostaria de apresentar uma proposta. Podemos bater um papo?"
- "Olá {name}! Vi o perfil de vocês online e tenho algo que pode interessar. Quando poderíamos conversar?"

## ⚙️ Configurações Avançadas

### Arquivo .env Completo

```bash
# API Keys
OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui

# Configurações do WhatsApp
WHATSAPP_SESSION_PATH=./baileys_auth_info

# Configurações de mensagens
DEFAULT_DELAY_SECONDS=5
MAX_MESSAGES_PER_HOUR=60

# Configurações da API
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
DEFAULT_MODEL=deepseek/deepseek-r1-0528:free
MESSAGE_TEMPERATURE=0.8
MAX_MESSAGE_TOKENS=150
```

### Formatos de Arquivo Suportados

**Excel (.xlsx)**:
```
| name                    | phone_number  | address              |
|------------------------|---------------|---------------------|
| Clínica Veterinária    | 11999887766   | Rua das Flores, 123 |
| Pet Shop Central       | 11888777655   | Av. Principal, 456   |
```

**CSV (.csv)**:
```csv
name,phone_number,address
"Clínica Veterinária","11999887766","Rua das Flores, 123"
"Pet Shop Central","11888777655","Av. Principal, 456"
```

## 🔧 Solução de Problemas

### QR Code não aparece
- Verifique se o Node.js está instalado: `node --version`
- Limpe a sessão: exclua a pasta `baileys_auth_info`
- Execute novamente

### Erro de API OpenRouter
- Verifique se a chave está correta no arquivo `.env`
- Confirme se tem créditos na conta OpenRouter
- Use o modelo gratuito: `deepseek/deepseek-r1-0528:free`

### Mensagens não enviando
- Confirme que o WhatsApp está conectado (status no banner)
- Verifique formato dos números: `11999887766` (DDD + número)
- Teste com um número conhecido primeiro

### Sessão desconectada
- O WhatsApp pode desconectar após 14 dias de inatividade
- Simplesmente escaneie o QR Code novamente
- Suas configurações serão mantidas

## 🛡️ Boas Práticas

### Limites e Segurança
- **Delay mínimo**: 5 segundos entre mensagens
- **Máximo diário**: Até 100 mensagens (recomendado)
- **Horário**: Evite envios após 20h e antes das 8h
- **Teste sempre**: Use um número seu para testar primeiro

### Mensagens Eficazes
- **Personalização**: Sempre use `{name}` no template
- **Concisão**: Máximo 2 linhas por mensagem
- **Propósito claro**: Seja direto sobre o motivo do contato
- **Call-to-action**: Termine com uma pergunta ou convite

## 🎉 Recursos Futuros

- [ ] Dashboard web para monitoramento
- [ ] Agendamento de disparos
- [ ] Relatórios de conversão
- [ ] Templates pré-definidos por setor
- [ ] Resposta automática a mensagens
- [ ] Integração com CRM

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este README primeiro
2. Teste com um número conhecido
3. Confirme configurações do `.env`
4. Reinicie o sistema se necessário

---

**🔥 ASIMOV LeadCaptor - Automatize sua prospecção com inteligência!**