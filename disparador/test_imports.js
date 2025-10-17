// Teste de importações
console.log("🔍 Testando importações...");

try {
    const baileys = require("@whiskeysockets/baileys");
    console.log("✅ Baileys importado com sucesso");
    console.log("Funções disponíveis:", Object.keys(baileys).slice(0, 10));
} catch (error) {
    console.log("❌ Erro ao importar Baileys:", error.message);
}

try {
    const fs = require("fs");
    console.log("✅ FS importado com sucesso");
} catch (error) {
    console.log("❌ Erro ao importar FS:", error.message);
}

try {
    const chalk = require("chalk");
    console.log("✅ Chalk importado com sucesso");
} catch (error) {
    console.log("❌ Erro ao importar Chalk:", error.message);
}

try {
    const xlsx = require("xlsx");
    console.log("✅ XLSX importado com sucesso");
} catch (error) {
    console.log("❌ Erro ao importar XLSX:", error.message);
}

try {
    const OpenAI = require("openai");
    console.log("✅ OpenAI importado com sucesso");
} catch (error) {
    console.log("❌ Erro ao importar OpenAI:", error.message);
}

console.log("🎯 Teste de importações concluído!");
