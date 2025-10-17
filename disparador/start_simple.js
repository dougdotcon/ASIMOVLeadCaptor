console.log("🔥 Iniciando ASIMOV LeadCaptor - WhatsApp Bot...");

// Importações básicas
const {
    makeWASocket,
    DisconnectReason,
    useMultiFileAuthState,
    Browsers,
} = require("@whiskeysockets/baileys");

const chalk = require("chalk");
const qrcode = require("qrcode-terminal");
const Pino = require("pino");

async function startBot() {
    console.log(chalk.green("📱 Configurando WhatsApp..."));
    
    try {
        const { state, saveCreds } = await useMultiFileAuthState("yusril");
        
        // Configurar logger adequado
        const logger = Pino({ level: 'silent' });
        
        const sock = makeWASocket({
            auth: state,
            logger: logger,
            browser: Browsers.macOS('Chrome'),
        });

        sock.ev.on('creds.update', saveCreds);
        
        sock.ev.on('connection.update', (update) => {
            const { connection, lastDisconnect, qr } = update;
            
            if (qr) {
                console.log(chalk.cyan('\n📱 QR Code para conectar ao WhatsApp:'));
                console.log(chalk.white('━'.repeat(50)));
                // QR Code em branco
                qrcode.generate(qr, { small: true }, (qrString) => {
                    console.log(chalk.white(qrString));
                });
                console.log(chalk.white('━'.repeat(50)));
                console.log(chalk.green('📱 Escaneie o QR Code acima com seu WhatsApp'));
                console.log(chalk.blue('💡 WhatsApp > Menu > Aparelhos conectados > Conectar aparelho'));
            }
            
            if (connection === 'close') {
                const shouldReconnect = (lastDisconnect?.error)?.output?.statusCode !== DisconnectReason.loggedOut;
                console.log(chalk.red('🔌 Conexão fechada:'), lastDisconnect.error, chalk.yellow('Reconectando:'), shouldReconnect);
                
                if (shouldReconnect) {
                    startBot();
                }
            } else if (connection === 'open') {
                console.log(chalk.green('✅ Conectado ao WhatsApp com sucesso!'));
                console.log(chalk.cyan(`
╔════════════════════════════════════════════════════════════════════╗
║                🔥 ASIMOV LeadCaptor - WhatsApp Bot                 ║
║                     Sistema Ativo e Funcionando                   ║
╠════════════════════════════════════════════════════════════════════╣
║  ✅ WhatsApp conectado                                             ║
║  📱 Pronto para receber comandos                                   ║
║  💬 Digite /menu para ver os comandos disponíveis                 ║
╚════════════════════════════════════════════════════════════════════╝
                `));
                
                // Enviar mensagem de confirmação para o próprio número
                const botNumber = sock.user.id;
                sock.sendMessage(botNumber, { 
                    text: `🔥 *ASIMOV LeadCaptor Ativo!*\n\n✅ Sistema inicializado com sucesso\n📱 Digite */menu* para ver os comandos\n\n🎯 Pronto para automatizar sua prospecção!` 
                });
            }
        });

        // Processar mensagens recebidas
        sock.ev.on('messages.upsert', async (m) => {
            const message = m.messages[0];
            if (!message.message || message.key.fromMe) return;
            
            const text = message.message.conversation || 
                        message.message.extendedTextMessage?.text || '';
            
            if (text.startsWith('/')) {
                const command = text.slice(1).toLowerCase();
                const from = message.key.remoteJid;
                
                switch (command) {
                    case 'menu':
                    case 'help':
                        await sock.sendMessage(from, {
                            text: `🔥 *ASIMOV LeadCaptor - Menu Principal*

🤖 *Comandos de IA:*
/ai [pergunta] - Chat com ChatGPT
/img [descrição] - Gerar imagem com DALL-E

📨 *Sistema de Envio em Massa:*
/mass - Acessar sistema completo
/testeenvio [número] [mensagem] - Teste rápido
/stats - Ver estatísticas

⚙️ *Sistema:*
/config - Ver configurações
/help - Este menu

🎯 *Sistema funcionando perfeitamente!*`
                        });
                        break;
                        
                    case 'test':
                    case 'teste':
                        await sock.sendMessage(from, {
                            text: '✅ Sistema ASIMOV LeadCaptor funcionando perfeitamente!\n\n🔥 Pronto para automação de WhatsApp!'
                        });
                        break;
                        
                    default:
                        await sock.sendMessage(from, {
                            text: `❓ Comando não reconhecido: /${command}\n\nDigite */menu* para ver os comandos disponíveis.`
                        });
                }
            }
        });

    } catch (error) {
        console.error(chalk.red('❌ Erro ao inicializar:'), error);
    }
}

// Iniciar o bot
startBot().catch(console.error);

console.log(chalk.blue("🚀 Sistema iniciado! Aguardando QR Code..."));
