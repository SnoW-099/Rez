@echo off
echo Iniciando la aplicacion completa...

REM Iniciar el backend en una ventana separada
start "Backend Server" cmd /k "cd /d ..\backend && python main.py"

REM Esperar un momento para que el backend inicie
timeout /t 5 /nobreak >nul

REM Iniciar el frontend
echo Iniciando el frontend...
cd /d frontend
npm start