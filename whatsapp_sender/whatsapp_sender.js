#!/usr/bin/env node
import { Boom } from '@hapi/boom'
import makeWASocket, { 
    DisconnectReason, 
    useMultiFileAuthState,
    MessageType,
    MessageOptions,
    Mimetype
} from '@whiskeysockets/baileys'
import qrcode from 'qrcode-terminal'
import fs from 'fs-extra'
import path from 'path'
import { fileURLToPath } from 'url'
import xlsx from 'xlsx'
import { OpenAI } from 'openai'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

class WhatsAppSender {
    constructor() {
        this.sock = null
        this.isConnected = false
        this.sessionPath = path.join(__dirname, 'baileys_auth_info')
        this.openaiClient = null
        this.initOpenAI()
    }

    initOpenAI() {
        // Configurar cliente OpenRouter
        this.openaiClient = new OpenAI({
            baseURL: "https://openrouter.ai/api/v1",
            apiKey: process.env.OPENROUTER_API_KEY || "seu_api_key_aqui",
            defaultHeaders: {
                "HTTP-Referer": "https://asimov-leadcaptor.local",
                "X-Title": "ASIMOV LeadCaptor"
            }
        })
    }

    async start() {
        console.log('🚀 Iniciando ASIMOV WhatsApp Sender...')
        
        try {
            await this.initializeWhatsApp()
        } catch (error) {
            console.error('❌ Erro ao inicializar WhatsApp:', error)
            throw error
        }
    }

    async initializeWhatsApp() {
        const { state, saveCreds } = await useMultiFileAuthState(this.sessionPath)
        
        this.sock = makeWASocket({
            auth: state,
            printQRInTerminal: true,
            logger: {
                level: 'silent'
            }
        })

        this.sock.ev.on('creds.update', saveCreds)
        
        this.sock.ev.on('connection.update', (update) => {
            const { connection, lastDisconnect, qr } = update
            
            if (qr) {
                console.log('📱 Escaneie o QR Code com seu WhatsApp:')
                qrcode.generate(qr, { small: true })
            }
            
            if (connection === 'close') {
                const shouldReconnect = (lastDisconnect?.error)?.output?.statusCode !== DisconnectReason.loggedOut
                console.log('🔌 Conexão fechada devido a:', lastDisconnect.error, ', reconectando:', shouldReconnect)
                
                if (shouldReconnect) {
                    this.initializeWhatsApp()
                }
            } else if (connection === 'open') {
                console.log('✅ Conectado ao WhatsApp com sucesso!')
                this.isConnected = true
                this.showMenu()
            }
        })

        this.sock.ev.on('messages.upsert', (m) => {
            // Pode ser usado para responder mensagens automaticamente no futuro
        })
    }

    async showMenu() {
        console.log(`
╔════════════════════════════════════════════════════════════════════╗
║                    🔥 ASIMOV WhatsApp Sender                       ║
║                         Menu Principal                             ║
╠════════════════════════════════════════════════════════════════════╣
║  [1] 📄 Carregar arquivo Excel/CSV de contatos                    ║
║  [2] 📨 Enviar mensagens para contatos carregados                 ║  
║  [3] 🧪 Testar envio para um número específico                    ║
║  [4] 📊 Ver estatísticas de envio                                 ║
║  [5] ⚙️  Configurações                                             ║
║  [0] 🚪 Sair                                                       ║
╚════════════════════════════════════════════════════════════════════╝
        `)

        const choice = await this.getUserInput('Escolha uma opção: ')
        await this.handleMenuChoice(choice)
    }

    async handleMenuChoice(choice) {
        switch (choice) {
            case '1':
                await this.loadContactsFile()
                break
            case '2':
                await this.sendMessagesToContacts()
                break
            case '3':
                await this.testSendMessage()
                break
            case '4':
                await this.showStatistics()
                break
            case '5':
                await this.showSettings()
                break
            case '0':
                console.log('👋 Encerrando ASIMOV WhatsApp Sender...')
                process.exit(0)
                break
            default:
                console.log('❌ Opção inválida!')
                await this.showMenu()
        }
    }

    async loadContactsFile() {
        console.log('📄 Digite o caminho do arquivo Excel/CSV com os contatos:')
        const filePath = await this.getUserInput('Caminho do arquivo: ')
        
        try {
            if (filePath.endsWith('.xlsx') || filePath.endsWith('.xls')) {
                const workbook = xlsx.readFile(filePath)
                const sheetName = workbook.SheetNames[0]
                const worksheet = workbook.Sheets[sheetName]
                this.contacts = xlsx.utils.sheet_to_json(worksheet)
            } else if (filePath.endsWith('.csv')) {
                const workbook = xlsx.readFile(filePath)
                const sheetName = workbook.SheetNames[0]
                const worksheet = workbook.Sheets[sheetName]
                this.contacts = xlsx.utils.sheet_to_json(worksheet)
            }

            console.log(`✅ ${this.contacts.length} contatos carregados com sucesso!`)
            console.log('Exemplo de contato:', this.contacts[0])
            
        } catch (error) {
            console.error('❌ Erro ao carregar arquivo:', error.message)
        }
        
        await this.showMenu()
    }

    async generateMessageVariation(originalMessage, businessName) {
        try {
            const prompt = `Crie uma variação única e natural da seguinte mensagem de prospecção comercial, mantendo o mesmo propósito mas mudando as palavras e estrutura. A mensagem deve soar profissional mas amigável.

Mensagem original: "${originalMessage}"
Nome do negócio: "${businessName}"

Regras:
1. Manter o propósito de apresentação/contato inicial
2. Incluir o nome do negócio naturalmente
3. Ser concisa (máximo 2 frases)
4. Soar natural e não robotizada
5. Não usar palavras iguais da mensagem original

Retorne apenas a nova mensagem, sem aspas ou explicações:`

            const completion = await this.openaiClient.chat.completions.create({
                model: "deepseek/deepseek-r1-0528:free",
                messages: [{
                    role: "user",
                    content: prompt
                }],
                max_tokens: 150,
                temperature: 0.8
            })

            return completion.choices[0].message.content.trim()
        } catch (error) {
            console.error('❌ Erro ao gerar variação da mensagem:', error)
            // Fallback para template básico
            return `Olá, tudo bem? Vi o ${businessName} e gostaria de conversar sobre uma oportunidade interessante. Podemos conversar?`
        }
    }

    async sendMessagesToContacts() {
        if (!this.contacts || this.contacts.length === 0) {
            console.log('❌ Nenhum contato carregado! Carregue um arquivo primeiro.')
            await this.showMenu()
            return
        }

        console.log('📨 Configuração do envio de mensagens')
        const messageTemplate = await this.getUserInput('Digite o template da mensagem (use {name} para o nome): ')
        const delayBetween = await this.getUserInput('Delay entre mensagens (segundos) [padrão: 5]: ') || '5'
        
        console.log(`\n🚀 Iniciando envio para ${this.contacts.length} contatos...`)
        
        let sent = 0
        let failed = 0
        
        for (let i = 0; i < this.contacts.length; i++) {
            const contact = this.contacts[i]
            const name = contact.name || contact.Name || contact.NOME || 'Cliente'
            const phone = this.formatPhoneNumber(contact.phone_number || contact.Phone || contact.TELEFONE || contact.phone)
            
            if (!phone) {
                console.log(`⚠️  Contato ${name} não tem telefone válido`)
                failed++
                continue
            }

            try {
                // Gerar variação única da mensagem
                const uniqueMessage = await this.generateMessageVariation(messageTemplate, name)
                
                console.log(`📤 Enviando para ${name} (${phone})...`)
                console.log(`📝 Mensagem: ${uniqueMessage}`)
                
                await this.sendMessage(phone, uniqueMessage)
                sent++
                
                console.log(`✅ Enviado para ${name}`)
                
                // Delay entre envios
                if (i < this.contacts.length - 1) {
                    console.log(`⏰ Aguardando ${delayBetween}s antes do próximo envio...`)
                    await this.sleep(parseInt(delayBetween) * 1000)
                }
                
            } catch (error) {
                console.error(`❌ Erro ao enviar para ${name}:`, error.message)
                failed++
            }
        }
        
        console.log(`\n📊 Resumo do envio:`)
        console.log(`✅ Enviadas: ${sent}`)
        console.log(`❌ Falharam: ${failed}`)
        console.log(`📱 Total: ${this.contacts.length}`)
        
        await this.showMenu()
    }

    async testSendMessage() {
        console.log('🧪 Teste de envio de mensagem')
        const phone = await this.getUserInput('Digite o número (com DDD, sem +55): ')
        const message = await this.getUserInput('Digite a mensagem: ')
        
        try {
            const formattedPhone = this.formatPhoneNumber(phone)
            console.log(`📤 Enviando mensagem teste para ${formattedPhone}...`)
            
            await this.sendMessage(formattedPhone, message)
            console.log('✅ Mensagem enviada com sucesso!')
            
        } catch (error) {
            console.error('❌ Erro ao enviar mensagem:', error.message)
        }
        
        await this.showMenu()
    }

    async sendMessage(phone, message) {
        if (!this.isConnected) {
            throw new Error('WhatsApp não está conectado')
        }

        const jid = `${phone}@s.whatsapp.net`
        
        try {
            await this.sock.sendMessage(jid, { text: message })
            return true
        } catch (error) {
            throw new Error(`Falha ao enviar mensagem: ${error.message}`)
        }
    }

    formatPhoneNumber(phone) {
        if (!phone) return null
        
        // Remove todos os caracteres não numéricos
        const cleaned = phone.toString().replace(/\D/g, '')
        
        // Se já tem código do país, mantém
        if (cleaned.startsWith('55') && cleaned.length >= 12) {
            return cleaned
        }
        
        // Se não tem código do país, adiciona 55
        if (cleaned.length >= 10) {
            return '55' + cleaned
        }
        
        return null
    }

    async showStatistics() {
        console.log('📊 Estatísticas ainda não implementadas')
        await this.showMenu()
    }

    async showSettings() {
        console.log('⚙️ Configurações ainda não implementadas')
        await this.showMenu()
    }

    getUserInput(question) {
        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        })
        
        return new Promise((resolve) => {
            readline.question(question, (answer) => {
                readline.close()
                resolve(answer)
            })
        })
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms))
    }
}

// Função principal
async function main() {
    const sender = new WhatsAppSender()
    
    try {
        await sender.start()
    } catch (error) {
        console.error('❌ Erro fatal:', error)
        process.exit(1)
    }
}

// Executar se chamado diretamente
if (import.meta.url === `file://${process.argv[1]}`) {
    main()
}

export default WhatsAppSender