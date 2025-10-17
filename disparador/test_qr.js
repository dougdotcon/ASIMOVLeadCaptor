const qrcode = require("qrcode-terminal");
const chalk = require("chalk");

console.log(chalk.cyan("🧪 Testando geração de QR Code..."));

// Teste com um QR Code simples
const testQR = "https://github.com/ASIMOV-LeadCaptor";

console.log(chalk.yellow('\n━'.repeat(50)));
console.log(chalk.green('📱 QR Code de teste:'));
qrcode.generate(testQR, { small: true });
console.log(chalk.yellow('━'.repeat(50)));

console.log(chalk.blue("✅ Se você vê um QR Code acima, a biblioteca está funcionando!"));
console.log(chalk.gray("🔗 QR Code aponta para: " + testQR));
