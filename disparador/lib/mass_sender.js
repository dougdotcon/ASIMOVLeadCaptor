const fs = require("fs");
const path = require("path");
const xlsx = require("xlsx");
const chalk = require("chalk");
const readline = require("readline");
const { OpenAI } = require("openai");
let setting = require("../key.json");

class MassSender {
    constructor(sock) {
        this.sock = sock;
        this.contacts = [];
        this.stats = {
            sent: 0,
            failed: 0,
            total: 0
        };
        this.isRunning = false;
        this.initOpenRouter();
    }

    initOpenRouter() {
        if (setting.openrouter_api_key && setting.openrouter_api_key !== "ISI_OPENROUTER_API_KEY_AQUI") {
            this.openaiClient = new OpenAI({
                baseURL: setting.openrouter_base_url,
                apiKey: setting.openrouter_api_key,
                defaultHeaders: {
                    "HTTP-Referer": "https://asimov-leadcaptor.local",
                    "X-Title": "ASIMOV LeadCaptor"
                }
            });
        } else {
            console.log(chalk.yellow("⚠️  OpenRouter API Key não configurada. Mensagens únicas desabilitadas."));
            console.log(chalk.blue("💡 Para habilitar mensagens únicas GRATUITAS:"));
            console.log(chalk.white("   1. Acesse: https://openrouter.ai"));
            console.log(chalk.white("   2. Crie conta gratuita"));
            console.log(chalk.white("   3. Obtenha API Key"));
            console.log(chalk.white("   4. Configure no arquivo key.json"));
            console.log(chalk.gray("   📄 Veja: CONFIGURAR_API.md para instruções completas\n"));
        }
    }

    async showMassMenu() {
        console.log(chalk.cyan(`
╔════════════════════════════════════════════════════════════════════╗
║                🔥 ASIMOV LeadCaptor - Envio em Massa               ║
╠════════════════════════════════════════════════════════════════════╣
║  [1] 📄 Carregar arquivo Excel/CSV de contatos                    ║
║  [2] 📨 Enviar mensagens para contatos carregados                 ║  
║  [3] 🧪 Testar envio para um número específico                    ║
║  [4] 📊 Ver estatísticas de envio                                 ║
║  [5] ⚙️  Configurações                                             ║
║  [6] 🔍 Visualizar contatos carregados                            ║
║  [0] ⬅️  Voltar ao menu principal                                  ║
╚════════════════════════════════════════════════════════════════════╝
        `));

        const choice = await this.getUserInput('Escolha uma opção: ');
        await this.handleMassMenuChoice(choice);
    }

    async handleMassMenuChoice(choice) {
        switch (choice) {
            case '1':
                await this.loadContactsFile();
                break;
            case '2':
                await this.sendMessagesToContacts();
                break;
            case '3':
                await this.testSendMessage();
                break;
            case '4':
                await this.showStatistics();
                break;
            case '5':
                await this.showSettings();
                break;
            case '6':
                await this.viewLoadedContacts();
                break;
            case '0':
                return false; // Voltar ao menu principal
            default:
                console.log(chalk.red('❌ Opção inválida!'));
                await this.showMassMenu();
        }
        return true;
    }

    async loadContactsFile() {
        console.log(chalk.cyan('📄 Carregamento de arquivo de contatos'));
        console.log('Formatos suportados: .xlsx, .xls, .csv');
        console.log('Colunas esperadas: name/Name/NOME, phone_number/Phone/TELEFONE/phone');
        
        const filePath = await this.getUserInput('Digite o caminho do arquivo: ');
        
        try {
            if (!fs.existsSync(filePath)) {
                console.log(chalk.red('❌ Arquivo não encontrado!'));
                await this.showMassMenu();
                return;
            }

            const workbook = xlsx.readFile(filePath);
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            this.contacts = xlsx.utils.sheet_to_json(worksheet);

            if (this.contacts.length === 0) {
                console.log(chalk.red('❌ Nenhum contato encontrado no arquivo!'));
                await this.showMassMenu();
                return;
            }

            console.log(chalk.green(`✅ ${this.contacts.length} contatos carregados com sucesso!`));
            
            // Mostrar exemplo do primeiro contato
            if (this.contacts[0]) {
                console.log(chalk.yellow('📋 Exemplo de contato:'));
                console.log(JSON.stringify(this.contacts[0], null, 2));
            }

            // Validar estrutura dos dados
            const validContacts = this.validateContacts();
            console.log(chalk.blue(`📊 Contatos válidos: ${validContacts}/${this.contacts.length}`));
            
        } catch (error) {
            console.log(chalk.red('❌ Erro ao carregar arquivo:', error.message));
        }
        
        await this.showMassMenu();
    }

    validateContacts() {
        let validCount = 0;
        this.contacts.forEach(contact => {
            const name = contact.name || contact.Name || contact.NOME || 'Cliente';
            const phone = contact.phone_number || contact.Phone || contact.TELEFONE || contact.phone;
            
            if (name && phone && this.formatPhoneNumber(phone)) {
                validCount++;
            }
        });
        return validCount;
    }

    async viewLoadedContacts() {
        if (!this.contacts || this.contacts.length === 0) {
            console.log(chalk.red('❌ Nenhum contato carregado!'));
            await this.showMassMenu();
            return;
        }

        console.log(chalk.cyan(`\n📋 Contatos carregados (${this.contacts.length} total):`));
        console.log(chalk.gray('─'.repeat(80)));

        this.contacts.slice(0, 10).forEach((contact, index) => {
            const name = contact.name || contact.Name || contact.NOME || 'Cliente';
            const phone = contact.phone_number || contact.Phone || contact.TELEFONE || contact.phone;
            const formattedPhone = this.formatPhoneNumber(phone);
            
            console.log(chalk.white(`${index + 1}. ${name}`));
            console.log(chalk.gray(`   📞 ${phone} ${formattedPhone ? '✅' : '❌'}`));
        });

        if (this.contacts.length > 10) {
            console.log(chalk.gray(`... e mais ${this.contacts.length - 10} contatos`));
        }

        await this.getUserInput('\nPressione Enter para continuar...');
        await this.showMassMenu();
    }

    async sendMessagesToContacts() {
        if (!this.contacts || this.contacts.length === 0) {
            console.log(chalk.red('❌ Nenhum contato carregado! Carregue um arquivo primeiro.'));
            await this.showMassMenu();
            return;
        }

        console.log(chalk.cyan('📨 Configuração do envio de mensagens'));
        
        const messageTemplate = await this.getUserInput('Digite o template da mensagem (use {name} para o nome): ');
        if (!messageTemplate.trim()) {
            console.log(chalk.red('❌ Template de mensagem não pode estar vazio!'));
            await this.showMassMenu();
            return;
        }

        const delayInput = await this.getUserInput(`Delay entre mensagens (segundos) [padrão: ${setting.default_delay_seconds}]: `);
        const delayBetween = delayInput || setting.default_delay_seconds.toString();
        
        const useAI = this.openaiClient ? await this.getUserInput('Usar IA para gerar mensagens únicas? (s/n) [padrão: s]: ') : 'n';
        const generateUnique = useAI.toLowerCase() !== 'n';

        console.log(chalk.yellow('\n📋 Configuração do envio:'));
        console.log(`📝 Template: ${messageTemplate}`);
        console.log(`⏰ Delay: ${delayBetween}s`);
        console.log(`🤖 IA ativada: ${generateUnique ? 'Sim' : 'Não'}`);
        console.log(`📊 Total de contatos: ${this.contacts.length}`);

        const confirm = await this.getUserInput('\nConfirmar envio? (s/n): ');
        if (confirm.toLowerCase() !== 's') {
            console.log(chalk.yellow('❌ Envio cancelado pelo usuário.'));
            await this.showMassMenu();
            return;
        }

        await this.startMassSending(messageTemplate, parseInt(delayBetween), generateUnique);
    }

    async startMassSending(messageTemplate, delayBetween, generateUnique) {
        console.log(chalk.green(`\n🚀 Iniciando envio para ${this.contacts.length} contatos...`));
        
        this.isRunning = true;
        this.stats = { sent: 0, failed: 0, total: this.contacts.length };
        
        for (let i = 0; i < this.contacts.length && this.isRunning; i++) {
            const contact = this.contacts[i];
            const name = contact.name || contact.Name || contact.NOME || 'Cliente';
            const phone = this.formatPhoneNumber(contact.phone_number || contact.Phone || contact.TELEFONE || contact.phone);
            
            if (!phone) {
                console.log(chalk.yellow(`⚠️  Contato ${name} não tem telefone válido`));
                this.stats.failed++;
                continue;
            }

            try {
                let finalMessage = messageTemplate.replace(/{name}/g, name);
                
                // Gerar mensagem única com IA se habilitado
                if (generateUnique && this.openaiClient) {
                    try {
                        finalMessage = await this.generateMessageVariation(messageTemplate, name);
                    } catch (error) {
                        console.log(chalk.yellow(`⚠️  Erro na IA para ${name}, usando template padrão`));
                        finalMessage = messageTemplate.replace(/{name}/g, name);
                    }
                }
                
                console.log(chalk.blue(`📤 [${i + 1}/${this.contacts.length}] Enviando para ${name} (${phone})...`));
                console.log(chalk.gray(`📝 Mensagem: ${finalMessage.substring(0, 100)}${finalMessage.length > 100 ? '...' : ''}`));
                
                await this.sendMessage(phone, finalMessage);
                this.stats.sent++;
                
                console.log(chalk.green(`✅ Enviado para ${name}`));
                
                // Delay entre envios
                if (i < this.contacts.length - 1) {
                    console.log(chalk.gray(`⏰ Aguardando ${delayBetween}s antes do próximo envio...`));
                    await this.sleep(delayBetween * 1000);
                }
                
            } catch (error) {
                console.log(chalk.red(`❌ Erro ao enviar para ${name}: ${error.message}`));
                this.stats.failed++;
            }
        }
        
        this.isRunning = false;
        await this.showFinalStats();
        await this.showMassMenu();
    }

    async generateMessageVariation(originalMessage, businessName) {
        if (!this.openaiClient) {
            throw new Error('Cliente OpenRouter não inicializado');
        }

        const prompt = `Crie uma variação única e natural da seguinte mensagem de prospecção comercial, mantendo o mesmo propósito mas mudando as palavras e estrutura. A mensagem deve soar profissional mas amigável.

Mensagem original: "${originalMessage}"
Nome do negócio: "${businessName}"

Regras:
1. Manter o propósito de apresentação/contato inicial
2. Incluir o nome do negócio naturalmente
3. Ser concisa (máximo 2 frases)
4. Soar natural e não robotizada
5. Não usar palavras iguais da mensagem original

Retorne apenas a nova mensagem, sem aspas ou explicações:`;

        const completion = await this.openaiClient.chat.completions.create({
            model: setting.default_model,
            messages: [{
                role: "user",
                content: prompt
            }],
            max_tokens: setting.max_message_tokens,
            temperature: setting.message_temperature
        });

        return completion.choices[0].message.content.trim();
    }

    async testSendMessage() {
        console.log(chalk.cyan('🧪 Teste de envio de mensagem'));
        const phone = await this.getUserInput('Digite o número (com DDD, sem +55): ');
        const message = await this.getUserInput('Digite a mensagem: ');
        
        try {
            const formattedPhone = this.formatPhoneNumber(phone);
            if (!formattedPhone) {
                console.log(chalk.red('❌ Número de telefone inválido!'));
                await this.showMassMenu();
                return;
            }

            console.log(chalk.blue(`📤 Enviando mensagem teste para ${formattedPhone}...`));
            
            await this.sendMessage(formattedPhone, message);
            console.log(chalk.green('✅ Mensagem enviada com sucesso!'));
            
        } catch (error) {
            console.log(chalk.red('❌ Erro ao enviar mensagem:', error.message));
        }
        
        await this.showMassMenu();
    }

    async sendMessage(phone, message) {
        const jid = `${phone}@s.whatsapp.net`;
        
        try {
            await this.sock.sendMessage(jid, { text: message });
            return true;
        } catch (error) {
            throw new Error(`Falha ao enviar mensagem: ${error.message}`);
        }
    }

    formatPhoneNumber(phone) {
        if (!phone) return null;
        
        // Remove todos os caracteres não numéricos
        const cleaned = phone.toString().replace(/\D/g, '');
        
        // Se já tem código do país, mantém
        if (cleaned.startsWith('55') && cleaned.length >= 12) {
            return cleaned;
        }
        
        // Se não tem código do país, adiciona 55
        if (cleaned.length >= 10) {
            return '55' + cleaned;
        }
        
        return null;
    }

    async showStatistics() {
        console.log(chalk.cyan(`
╔════════════════════════════════════════════════════════════════════╗
║                        📊 Estatísticas de Envio                   ║
╠════════════════════════════════════════════════════════════════════╣
║  📤 Mensagens enviadas: ${this.stats.sent.toString().padStart(10)}                      ║
║  ❌ Mensagens falharam: ${this.stats.failed.toString().padStart(10)}                      ║
║  📱 Total de contatos:  ${this.stats.total.toString().padStart(10)}                      ║
║  📋 Contatos carregados: ${this.contacts.length.toString().padStart(9)}                      ║
║  🔄 Status: ${(this.isRunning ? 'Executando' : 'Parado').padStart(17)}                      ║
╚════════════════════════════════════════════════════════════════════╝
        `));

        if (this.stats.total > 0) {
            const successRate = ((this.stats.sent / this.stats.total) * 100).toFixed(1);
            console.log(chalk.green(`📈 Taxa de sucesso: ${successRate}%`));
        }

        await this.getUserInput('\nPressione Enter para continuar...');
        await this.showMassMenu();
    }

    async showFinalStats() {
        console.log(chalk.cyan(`
╔════════════════════════════════════════════════════════════════════╗
║                    🎯 Resumo Final do Envio                       ║
╠════════════════════════════════════════════════════════════════════╣`));
        console.log(chalk.green(`║  ✅ Enviadas com sucesso: ${this.stats.sent.toString().padStart(6)}                          ║`));
        console.log(chalk.red(`║  ❌ Falharam:             ${this.stats.failed.toString().padStart(6)}                          ║`));
        console.log(chalk.blue(`║  📱 Total processados:    ${this.stats.total.toString().padStart(6)}                          ║`));
        
        if (this.stats.total > 0) {
            const successRate = ((this.stats.sent / this.stats.total) * 100).toFixed(1);
            console.log(chalk.yellow(`║  📈 Taxa de sucesso:      ${successRate.padStart(6)}%                         ║`));
        }
        
        console.log(chalk.cyan(`╚════════════════════════════════════════════════════════════════════╝`));
    }

    async showSettings() {
        console.log(chalk.cyan(`
╔════════════════════════════════════════════════════════════════════╗
║                          ⚙️ Configurações                          ║
╠════════════════════════════════════════════════════════════════════╣
║  OpenAI API Key: ${setting.keyopenai !== 'ISI_APIKEY_OPENAI_DISINI' ? '✅ Configurada' : '❌ Não configurada'}                    ║
║  OpenRouter API Key: ${setting.openrouter_api_key !== 'ISI_OPENROUTER_API_KEY_AQUI' ? '✅ Configurada' : '❌ Não configurada'}               ║
║  Modelo padrão: ${setting.default_model.padEnd(20)}                     ║
║  Delay padrão: ${setting.default_delay_seconds}s                                      ║
║  Max mensagens/hora: ${setting.max_messages_per_hour}                                ║
╚════════════════════════════════════════════════════════════════════╝
        `));

        console.log(chalk.yellow('\n💡 Para alterar as configurações, edite o arquivo key.json'));
        await this.getUserInput('\nPressione Enter para continuar...');
        await this.showMassMenu();
    }

    getUserInput(question) {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        return new Promise((resolve) => {
            rl.question(question, (answer) => {
                rl.close();
                resolve(answer);
            });
        });
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    stopSending() {
        this.isRunning = false;
        console.log(chalk.yellow('\n⏹️  Parando envio de mensagens...'));
    }
}

module.exports = MassSender;
