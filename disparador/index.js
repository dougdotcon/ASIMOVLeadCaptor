process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
const {
	makeWASocket,
	fetchLatestBaileysVersion,
	DisconnectReason,
	useMultiFileAuthState,
	makeCacheableSignalKeyStore,
	Browsers,
} = require("@whiskeysockets/baileys");

// Importar makeInMemoryStore separadamente se disponível
let makeInMemoryStore;
try {
	makeInMemoryStore = require("@whiskeysockets/baileys").makeInMemoryStore;
} catch (error) {
	console.log("makeInMemoryStore não disponível nesta versão do Baileys");
}
const fs = require("fs");
const Pino = require("pino");
const chalk = require("chalk");
const qrcode = require("qrcode-terminal");
const moment = require("moment-timezone");
// Configurar timezone para Brasil
moment.tz.setDefault("America/Sao_Paulo").locale("pt-br");
const { Messages } = require("./lib/messages.js");
const donet = "https://saweria.co/sansekai";

// Baileys
const Logger = {
	level: "error",
};
const logger = Pino({
	...Logger,
});
const Store = (log = logger) => {
	if (makeInMemoryStore) {
		const store = makeInMemoryStore({ logger: log });
		return store;
	}
	return null;
};
const store = Store(logger);
if (store) {
	store.readFromFile("./session.json");
	setInterval(() => {
		store.writeToFile("./session.json");
	}, 10_000);
}

const color = (text, color) => {
  return !color ? chalk.green(text) : chalk.keyword(color)(text);
};

async function connectToWhatsApp(use_pairing_code = false) {
	const { state, saveCreds } = await useMultiFileAuthState("yusril");

	const { version } = await fetchLatestBaileysVersion();
	const sock = makeWASocket({
		auth: {
			creds: state.creds,
			keys: makeCacheableSignalKeyStore(state.keys, logger),
		},
		version: version,
		logger: logger,
    markOnlineOnConnect: true,
		generateHighQualityLinkPreview: true,
		browser: Browsers.macOS('Chrome'),
    getMessage
	});

	if (store) {
		store.bind(sock.ev);
	}

	sock.ev.process(async (ev) => {
		if (ev["creds.update"]) {
			await saveCreds();
		}
		if (ev["connection.update"]) {
			console.log("Connection update", ev["connection.update"]);
			const update = ev["connection.update"];
			const { connection, lastDisconnect, qr } = update;
			
			// Gerar QR Code manualmente
			if (qr) {
				console.log(chalk.cyan('\n📱 QR Code para conectar ao WhatsApp:'));
				console.log(chalk.white('━'.repeat(60)));
				// QR Code em branco
				qrcode.generate(qr, { small: true }, (qrString) => {
					console.log(chalk.white(qrString));
				});
				console.log(chalk.white('━'.repeat(60)));
				console.log(chalk.green('📱 Escaneie o QR Code acima com seu WhatsApp'));
				console.log(chalk.blue('💡 WhatsApp > Menu > Aparelhos conectados > Conectar aparelho'));
				console.log(chalk.gray('⏳ Aguardando conexão...\n'));
			}
			if (connection === "close") {
				const shouldReconnect =
					lastDisconnect.error?.output?.statusCode !== DisconnectReason.loggedOut;
				console.log(
					"connection closed due to ",
					lastDisconnect.error,
					", reconnecting ",
					shouldReconnect
				);
				// reconnect if not logged out
				if (shouldReconnect) {
					connectToWhatsApp();
				}
			} else if (connection === "open") {
        const botNumber = sock.user.id
				console.log("opened connection");
        console.log(color("🔥 ASIMOV LeadCaptor conectado com sucesso!", "green"));
        console.log(color("Sistema de envio em massa ativo", "cyan"));
        console.log(color("Digite /menu no WhatsApp para ver os comandos", "yellow"));
        
        // Mostrar banner do sistema
        console.log(chalk.cyan(`
╔════════════════════════════════════════════════════════════════════╗
║                🔥 ASIMOV LeadCaptor - WhatsApp Bot                 ║
║                     Sistema Completo Ativo                        ║
╠════════════════════════════════════════════════════════════════════╣
║  ✅ WhatsApp conectado                                             ║
║  ✅ Sistema de IA ativo                                            ║
║  ✅ Envio em massa disponível                                      ║
║  ✅ Geração de mensagens únicas                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  📱 Comandos principais:                                           ║
║     /menu - Ver todos os comandos                                  ║
║     /mass - Sistema de envio em massa                              ║
║     /ai - Chat com IA                                              ║
║     /img - Gerar imagens                                           ║
╚════════════════════════════════════════════════════════════════════╝
        `));
        
        sock.sendMessage(botNumber, { text: `🔥 *ASIMOV LeadCaptor Ativo!*

✅ Sistema completo inicializado
🤖 IA e automação disponíveis
📨 Envio em massa configurado

Digite */menu* para ver todos os comandos

🎯 *Pronto para automatizar sua prospecção!*` });
			}
		}
    // sock.ev.on("messages.upsert", async (message) => { 
    //   console.log(message);
    // })
		
		const upsert = ev["messages.upsert"];
if (upsert) {
	if (upsert.type !== "notify") {
        return;
    }
    const message = Messages(upsert, sock);
    if (!message || message.sender === "status@broadcast") {
        return;
    }
    // msgHandler(upsert, sock, store, message);
	require("./sansekai.js")(upsert, sock, store, message);
 }

    
    //   const message = Messages(upsert, sock);
    //   console.log(message);
		// }
	});
	/**
	 *
	 * @param {import("@whiskeysockets/baileys").WAMessageKey} key
	 * @returns {import("@whiskeysockets/baileys").WAMessageContent | undefined}
	 */
	async function getMessage(key) {
		if (store) {
			const msg = await store.loadMessage(key.remoteJid, key.id);
			return msg?.message || undefined;
		}
		// Retornar undefined se não há store
		return undefined;
	}
	return sock;
}
connectToWhatsApp()
// Baileys

let file = require.resolve(__filename);
fs.watchFile(file, () => {
  fs.unwatchFile(file);
  console.log(chalk.redBright(`Update ${__filename}`));
  delete require.cache[file];
  require(file);
});