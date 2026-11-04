@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Primero prepara el entorno con las instrucciones de README.md.
    pause
    exit /b 1
)
set "PORT=5000"
echo CrediDSL disponible en http://127.0.0.1:5000
".venv\Scripts\python.exe" app.py
if errorlevel 1 pause
