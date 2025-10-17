@echo off
title ASIMOV LeadCaptor - Sistema Completo
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                🔥 ASIMOV LeadCaptor - Launcher                     ║
echo ║                    Sistema Completo Iniciando...                   ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.7+ primeiro.
    echo 💡 Download: https://python.org/downloads/
    pause
    exit /b 1
)

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado! Instale Node.js primeiro.
    echo 💡 Download: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Python e Node.js encontrados!
echo 🚀 Iniciando ASIMOV LeadCaptor...
echo.

REM Executar o launcher Python
python app.py

echo.
echo 👋 ASIMOV LeadCaptor encerrado.
pause
