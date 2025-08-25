@echo off
title ASIMOV LeadCaptor CYBERPUNK LAUNCHER
color 0A

echo.
echo ===============================================
echo    ASIMOV LeadCaptor CYBERPUNK LAUNCHER
echo ===============================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale o Python 3.7+ antes de continuar.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.

REM Executar o launcher Python
echo Iniciando interface cyberpunk...
python start_cyberpunk.py

REM Pausar no final para ver mensagens de erro se houver
if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um erro durante a execucao.
    pause
)

exit /b 0
