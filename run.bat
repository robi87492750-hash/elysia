@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
    echo First launch: installing the desktop pet runtime. This can take a few minutes.
    call setup.bat
    if errorlevel 1 exit /b 1
)

start "" ".venv\Scripts\pythonw.exe" main.py
