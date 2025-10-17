const { BufferJSON, WA_DEFAULT_EPHEMERAL, generateWAMessageFromContent, proto, generateWAMessageContent, generateWAMessage, prepareWAMessageMedia, areJidsSameUser, getContentType } = require("@whiskeysockets/baileys");
const fs = require("fs");
const util = require("util");
const chalk = require("chalk");
const OpenAI = require("openai");
const MassSender = require("./lib/mass_sender.js");
let setting = require("./key.json");
const openai = new OpenAI({ apiKey: setting.keyopenai });

// Instância global do MassSender
let massSender = null;

module.exports = sansekai = async (upsert, sock, store, message) => {
  try {
    // Inicializar MassSender se ainda não foi inicializado
    if (!massSender) {
      massSender = new MassSender(sock);
    }

    let budy = (typeof message.text == 'string' ? message.text : '')
    // var prefix = /^[\\/!#.]/gi.test(body) ? body.match(/^[\\/!#.]/gi) : "/"
    var prefix = /^[\\/!#.]/gi.test(budy) ? budy.match(/^[\\/!#.]/gi) : "/";
    const isCmd = budy.startsWith(prefix);
    const command = budy.replace(prefix, "").trim().split(/ +/).shift().toLowerCase();
    const args = budy.trim().split(/ +/).slice(1);
    const pushname = message.pushName || "No Name";
    const botNumber = sock.user.id;
    const itsMe = message.sender == botNumber ? true : false;
    let text = (q = args.join(" "));
    const arg = budy.trim().substring(budy.indexOf(" ") + 1);
    const arg1 = arg.trim().substring(arg.indexOf(" ") + 1);
    const from = message.chat;

    const color = (text, color) => {
      return !color ? chalk.green(text) : chalk.keyword(color)(text);
    };

    // Group
    const groupMetadata = message.isGroup ? await sock.groupMetadata(message.chat).catch((e) => {}) : "";
    const groupName = message.isGroup ? groupMetadata.subject : "";

    // Push Message To Console
    let argsLog = budy.length > 30 ? `${q.substring(0, 30)}...` : budy;

    if (isCmd && !message.isGroup) {
      console.log(chalk.black(chalk.bgWhite("[ LOGS ]")), color(argsLog, "turquoise"), chalk.magenta("From"), chalk.green(pushname), chalk.yellow(`[ ${message.sender.replace("@s.whatsapp.net", "")} ]`));
    } else if (isCmd && message.isGroup) {
      console.log(
        chalk.black(chalk.bgWhite("[ LOGS ]")),
        color(argsLog, "turquoise"),
        chalk.magenta("From"),
        chalk.green(pushname),
        chalk.yellow(`[ ${message.sender.replace("@s.whatsapp.net", "")} ]`),
        chalk.blueBright("IN"),
        chalk.green(groupName)
      );
    }

    if (isCmd) {
      switch (command) {
        case "help": case "menu": case "start": case "info":
          message.reply(`*🔥 ASIMOV LeadCaptor - WhatsApp Bot*

*🤖 IA & Automação:*
${prefix}ai - Chat com ChatGPT
${prefix}img - Gerar imagens com DALL-E
${prefix}mass - Sistema de envio em massa
${prefix}leadcaptor - Menu principal LeadCaptor

*📊 Envio em Massa:*
${prefix}loadcontacts - Carregar arquivo Excel/CSV
${prefix}sendmass - Enviar mensagens em massa
${prefix}testeenvio - Testar envio para um número
${prefix}stats - Ver estatísticas de envio

*⚙️ Sistema:*
${prefix}config - Ver configurações
${prefix}sc - Código fonte do bot
${prefix}help - Este menu

*🎯 ASIMOV LeadCaptor - Automatize sua prospecção!*`)
          break;
        case "ai": case "openai": case "chatgpt": case "ask":
          try {
            // tidak perlu diisi apikeynya disini, karena sudah diisi di file key.json
            if (setting.keyopenai === "ISI_APIKEY_OPENAI_DISINI") return message.reply("Apikey belum diisi\n\nSilahkan isi terlebih dahulu apikeynya di file key.json\n\nApikeynya bisa dibuat di website: https://beta.openai.com/account/api-keys");
            if (!text) return message.reply(`Chat dengan AI.\n\nContoh:\n${prefix}${command} Apa itu resesi`);
            const chatCompletion = await openai.chat.completions.create({
              messages: [{ role: 'user', content: q }],
              model: 'gpt-3.5-turbo'
            });
          
            await message.reply(chatCompletion.choices[0].message.content);
          } catch (error) {
          if (error.response) {
            console.log(error.response.status);
            console.log(error.response.data);
          } else {
            console.log(error);
            message.reply("Maaf, sepertinya ada yang error :"+ error.message);
          }
        }
          break;
        case "img": case "ai-img": case "image": case "images": case "dall-e": case "dalle":
          try {
            // tidak perlu diisi apikeynya disini, karena sudah diisi di file key.json
            if (setting.keyopenai === "ISI_APIKEY_OPENAI_DISINI") return message.reply("Apikey belum diisi\n\nSilahkan isi terlebih dahulu apikeynya di file key.json\n\nApikeynya bisa dibuat di website: https://beta.openai.com/account/api-keys");
            if (!text) return message.reply(`Membuat gambar dari AI.\n\nContoh:\n${prefix}${command} Wooden house on snow mountain`);
            const image = await openai.images.generate({ 
              model: "dall-e-3",
              prompt: q, 
              n: 1,
              size: '1024x1024' 
              });
            //console.log(response.data.data[0].url) // see the response
            sock.sendMessage(from, 
              { image: { url: image.data[0].url }, caption: "DALE-E" },
              { quoted: message, ephemeralExpiration: message.contextInfo.expiration });
            } catch (error) {
          if (error.response) {
            console.log(error.response.status);
            console.log(error.response.data);
            console.log(`${error.response.status}\n\n${error.response.data}`);
          } else {
            console.log(error);
            message.reply("Maaf, sepertinya ada yang error :"+ error.message);
          }
        }
          break;
          case "sc": case "script": case "scbot":
           message.reply("🔥 ASIMOV LeadCaptor - Sistema completo de automação WhatsApp\n\nBaseado em: https://github.com/Sansekai/Wa-OpenAI\nAdaptado para: Sistema de captura e envio de leads");
          break;

        // ===== COMANDOS DO SISTEMA DE ENVIO EM MASSA =====
        case "mass": case "leadcaptor": case "sistema":
          try {
            message.reply("🔥 *ASIMOV LeadCaptor - Sistema de Envio em Massa*\n\n⚠️ *ATENÇÃO:* Este sistema será executado via terminal/console.\n\nPara usar o sistema completo:\n1. Acesse o terminal onde o bot está rodando\n2. O menu interativo aparecerá automaticamente\n3. Ou use os comandos específicos aqui no WhatsApp\n\n*Comandos disponíveis:*\n/loadcontacts - Carregar contatos\n/sendmass - Envio em massa\n/testeenvio - Teste de envio\n/stats - Estatísticas");
            
            // Mostrar menu no terminal
            console.log(chalk.cyan('\n🔥 Sistema de envio em massa solicitado via WhatsApp!'));
            if (massSender) {
              setTimeout(() => {
                massSender.showMassMenu();
              }, 1000);
            }
          } catch (error) {
            message.reply("❌ Erro ao acessar sistema de envio em massa: " + error.message);
          }
          break;

        case "loadcontacts": case "carregar": case "contatos":
          message.reply("📄 *Carregamento de Contatos*\n\n⚠️ Esta função deve ser executada via terminal.\n\nPara carregar contatos:\n1. Prepare seu arquivo Excel (.xlsx) ou CSV\n2. Acesse o terminal onde o bot está rodando\n3. Use o menu interativo que aparecerá\n\n*Formato do arquivo:*\n- Colunas: name, phone_number\n- Exemplo: João Silva, 11999887766");
          
          console.log(chalk.cyan('\n📄 Carregamento de contatos solicitado via WhatsApp!'));
          if (massSender) {
            setTimeout(() => {
              massSender.loadContactsFile();
            }, 1000);
          }
          break;

        case "sendmass": case "enviarmassa": case "disparo":
          message.reply("📨 *Envio em Massa*\n\n⚠️ Esta função deve ser executada via terminal.\n\n*Pré-requisitos:*\n1. Contatos já carregados\n2. Template de mensagem definido\n3. Configurações de delay\n\nAcesse o terminal para continuar o processo.");
          
          console.log(chalk.cyan('\n📨 Envio em massa solicitado via WhatsApp!'));
          if (massSender) {
            setTimeout(() => {
              massSender.sendMessagesToContacts();
            }, 1000);
          }
          break;

        case "testeenvio": case "teste": case "testmsg":
          if (!text) {
            message.reply("🧪 *Teste de Envio*\n\nUso: /testeenvio [número] [mensagem]\n\nExemplo:\n/testeenvio 11999887766 Olá, esta é uma mensagem de teste!");
            break;
          }
          
          try {
            const parts = text.split(' ');
            const phone = parts[0];
            const testMessage = parts.slice(1).join(' ');
            
            if (!phone || !testMessage) {
              message.reply("❌ Formato incorreto!\n\nUso: /testeenvio [número] [mensagem]");
              break;
            }

            if (massSender) {
              const formattedPhone = massSender.formatPhoneNumber(phone);
              if (!formattedPhone) {
                message.reply("❌ Número de telefone inválido!");
                break;
              }

              await massSender.sendMessage(formattedPhone, testMessage);
              message.reply(`✅ Mensagem teste enviada com sucesso para ${formattedPhone}!\n\n📝 Mensagem: ${testMessage}`);
            } else {
              message.reply("❌ Sistema de envio não inicializado!");
            }
          } catch (error) {
            message.reply("❌ Erro ao enviar mensagem teste: " + error.message);
          }
          break;

        case "stats": case "estatisticas": case "relatorio":
          if (massSender) {
            const stats = massSender.stats;
            message.reply(`📊 *Estatísticas de Envio*

📤 Mensagens enviadas: ${stats.sent}
❌ Mensagens falharam: ${stats.failed}
📱 Total processados: ${stats.total}
📋 Contatos carregados: ${massSender.contacts.length}
🔄 Status: ${massSender.isRunning ? 'Executando' : 'Parado'}

${stats.total > 0 ? `📈 Taxa de sucesso: ${((stats.sent / stats.total) * 100).toFixed(1)}%` : ''}`);
          } else {
            message.reply("❌ Sistema de envio não inicializado!");
          }
          break;

        case "config": case "configuracoes": case "settings":
          message.reply(`⚙️ *Configurações do Sistema*

🤖 OpenAI API: ${setting.keyopenai !== 'ISI_APIKEY_OPENAI_DISINI' ? '✅ Configurada' : '❌ Não configurada'}
🔄 OpenRouter API: ${setting.openrouter_api_key !== 'ISI_OPENROUTER_API_KEY_AQUI' ? '✅ Configurada' : '❌ Não configurada'}
🎯 Modelo padrão: ${setting.default_model}
⏰ Delay padrão: ${setting.default_delay_seconds}s
📊 Max mensagens/hora: ${setting.max_messages_per_hour}

💡 Para alterar, edite o arquivo key.json`);
          break;

        case "stop": case "parar": case "cancelar":
          if (massSender && massSender.isRunning) {
            massSender.stopSending();
            message.reply("⏹️ Envio de mensagens interrompido!");
          } else {
            message.reply("ℹ️ Nenhum envio em andamento.");
          }
          break;
        default: {
          if (isCmd && budy.toLowerCase() != undefined) {
            if (message.chat.endsWith("broadcast")) return;
            if (message.isBaileys) return;
            if (!budy.toLowerCase()) return;
            if (argsLog || (isCmd && !message.isGroup)) {
              // sock.sendReadReceipt(message.chat, message.sender, [message.key.id])
              console.log(chalk.black(chalk.bgRed("[ ERROR ]")), color("command", "turquoise"), color(`${prefix}${command}`, "turquoise"), color("tidak tersedia", "turquoise"));
            } else if (argsLog || (isCmd && message.isGroup)) {
              // sock.sendReadReceipt(message.chat, message.sender, [message.key.id])
              console.log(chalk.black(chalk.bgRed("[ ERROR ]")), color("command", "turquoise"), color(`${prefix}${command}`, "turquoise"), color("tidak tersedia", "turquoise"));
            }
          }
        }
      }
    }
  } catch (err) {
    message.reply(util.format(err));
  }
};

let file = require.resolve(__filename);
fs.watchFile(file, () => {
  fs.unwatchFile(file);
  console.log(chalk.redBright(`Update ${__filename}`));
  delete require.cache[file];
  require(file);
});
