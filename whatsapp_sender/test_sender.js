#!/usr/bin/env node
/**
 * Script de teste para validar a configuração do WhatsApp Sender
 */

import fs from 'fs-extra'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

console.log('🧪 ASIMOV WhatsApp Sender - Teste de Configuração\n')

// Teste 1: Verificar dependências
console.log('📦 Verificando dependências...')

try {
    // Testar import do Baileys
    await import('@whiskeysockets/baileys')
    console.log('✅ Baileys: OK')
} catch (error) {
    console.log('❌ Baileys: ERRO -', error.message)
}

try {
    // Testar import do QR Code
    await import('qrcode-terminal')
    console.log('✅ QR Code Terminal: OK')
} catch (error) {
    console.log('❌ QR Code Terminal: ERRO -', error.message)
}

try {
    // Testar import do OpenAI
    const { OpenAI } = await import('openai')
    console.log('✅ OpenAI SDK: OK')
} catch (error) {
    console.log('❌ OpenAI SDK: ERRO -', error.message)
}

try {
    // Testar import do XLSX
    await import('xlsx')
    console.log('✅ XLSX: OK')
} catch (error) {
    console.log('❌ XLSX: ERRO -', error.message)
}

// Teste 2: Verificar arquivo .env
console.log('\n⚙️ Verificando configurações...')

const envPath = path.join(__dirname, '.env')
if (fs.existsSync(envPath)) {
    console.log('✅ Arquivo .env encontrado')
    
    const envContent = fs.readFileSync(envPath, 'utf8')
    
    if (envContent.includes('OPENROUTER_API_KEY=')) {
        const match = envContent.match(/OPENROUTER_API_KEY=(.+)/)
        if (match && match[1] && match[1] !== 'seu_openrouter_api_key_aqui') {
            console.log('✅ API Key OpenRouter configurada')
        } else {
            console.log('⚠️ API Key OpenRouter não configurada adequadamente')
        }
    } else {
        console.log('❌ OPENROUTER_API_KEY não encontrada no .env')
    }
} else {
    console.log('⚠️ Arquivo .env não encontrado')
    console.log('💡 Copie .env.example para .env e configure suas chaves')
}

// Teste 3: Verificar estrutura de pastas
console.log('\n📁 Verificando estrutura de arquivos...')

const requiredFiles = [
    'package.json',
    'whatsapp_sender.js',
    '.env.example'
]

requiredFiles.forEach(file => {
    const filePath = path.join(__dirname, file)
    if (fs.existsSync(filePath)) {
        console.log(`✅ ${file}`)
    } else {
        console.log(`❌ ${file}`)
    }
})

// Teste 4: Verificar Node.js version
console.log('\n🔧 Verificando versão do Node.js...')
console.log(`Node.js: ${process.version}`)

const nodeVersion = parseInt(process.version.replace('v', '').split('.')[0])
if (nodeVersion >= 16) {
    console.log('✅ Versão do Node.js compatível (>=16)')
} else {
    console.log('❌ Versão do Node.js muito antiga. Instale Node.js 16 ou superior')
}

// Teste 5: Teste de API OpenRouter (se configurada)
console.log('\n🌐 Testando conexão com OpenRouter...')

try {
    if (fs.existsSync(envPath)) {
        const envContent = fs.readFileSync(envPath, 'utf8')
        const match = envContent.match(/OPENROUTER_API_KEY=(.+)/)
        
        if (match && match[1] && match[1] !== 'seu_openrouter_api_key_aqui') {
            const { OpenAI } = await import('openai')
            
            const client = new OpenAI({
                baseURL: "https://openrouter.ai/api/v1",
                apiKey: match[1].trim(),
                defaultHeaders: {
                    "HTTP-Referer": "https://asimov-leadcaptor.test",
                    "X-Title": "ASIMOV LeadCaptor Test"
                }
            })

            const testPrompt = "Diga apenas 'teste ok' se você conseguir me ouvir."
            
            const completion = await client.chat.completions.create({
                model: "deepseek/deepseek-r1-0528:free",
                messages: [{
                    role: "user",
                    content: testPrompt
                }],
                max_tokens: 10
            })

            console.log('✅ Conexão com OpenRouter funcionando')
            console.log(`📝 Resposta de teste: ${completion.choices[0].message.content}`)
        } else {
            console.log('⚠️ API Key não configurada, pulando teste de conexão')
        }
    }
} catch (error) {
    console.log('❌ Erro ao testar OpenRouter:', error.message)
}

console.log('\n🎯 Resumo do Teste')
console.log('==================')
console.log('Se todos os itens estão ✅, você pode usar o WhatsApp Sender!')
console.log('Se há itens ❌ ou ⚠️, configure-os antes de usar.')
console.log('\n💡 Para usar o sistema:')
console.log('1. Configure o .env com sua API key')
console.log('2. Execute: node whatsapp_sender.js')
console.log('3. Escaneie o QR Code com WhatsApp')
console.log('4. Divirta-se! 🚀')