@echo off
title ASIMOV LeadCaptor - Kill Chrome Processes
color 0C

echo.
echo ===============================================
echo    ASIMOV LeadCaptor - Kill Chrome Processes
echo ===============================================
echo.

echo Matando processos do Chrome...
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im chromedriver.exe >nul 2>&1

echo Matando processos do WebDriver...
taskkill /f /im python.exe /fi "WINDOWTITLE eq *cyberpunk*" >nul 2>&1

echo.
echo ✅ Processos finalizados!
echo Agora você pode executar o sistema novamente.
echo.

pause
