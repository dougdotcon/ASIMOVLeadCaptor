# 🔑 Como Configurar APIs - ASIMOV LeadCaptor

## 🚀 OpenRouter (Para Mensagens Únicas) - GRATUITO

### 1. Criar Conta OpenRouter
1. Acesse: https://openrouter.ai
2. Clique em "Sign Up" 
3. Faça login com Google/GitHub ou crie conta

### 2. Obter API Key GRATUITA
1. Vá em: https://openrouter.ai/keys
2. Clique em "Create Key"
3. Copie a chave (começa com `sk-or-v1-...`)

### 3. Configurar no Sistema
Edite o arquivo `key.json`:

```json
{
  "keyopenai": "ISI_APIKEY_OPENAI_DISINI",
  "openrouter_api_key": "sk-or-v1-SUA-CHAVE-AQUI",
  "openrouter_base_url": "https://openrouter.ai/api/v1",
  "default_model": "deepseek/deepseek-r1-0528:free",
  "message_temperature": 0.8,
  "max_message_tokens": 150,
  "default_delay_seconds": 5,
  "max_messages_per_hour": 60
}
```

### 4. Reiniciar Sistema
```bash
# Parar o sistema atual (Ctrl+C)
# Executar novamente:
node index.js
```

## 🤖 OpenAI (Opcional - Para /ai e /img)

### 1. Criar Conta OpenAI
1. Acesse: https://platform.openai.com
2. Crie conta e adicione método de pagamento

### 2. Obter API Key
1. Vá em: https://platform.openai.com/api-keys
2. Clique em "Create new secret key"
3. Copie a chave (começa com `sk-...`)

### 3. Configurar
No arquivo `key.json`, substitua:
```json
{
  "keyopenai": "sk-SUA-CHAVE-OPENAI-AQUI"
}
```

## ✅ Verificar Configuração

Após configurar, o sistema mostrará:
- ✅ OpenRouter API: Configurada
- ✅ Mensagens únicas habilitadas

## 🎯 Funcionalidades Habilitadas

### Com OpenRouter:
- 🧠 Mensagens únicas para cada contato
- 🔄 Variações automáticas de templates
- 📊 Envio em massa inteligente

### Com OpenAI:
- 🤖 Chat com IA via `/ai`
- 🎨 Geração de imagens via `/img`

---

**💡 Dica:** O OpenRouter é GRATUITO e suficiente para mensagens únicas!
