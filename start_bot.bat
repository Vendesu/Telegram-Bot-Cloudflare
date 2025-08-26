@echo off
chcp 65001 >nul
title Bot Cloudflare Pro - Startup Script

echo 🚀 Starting Bot Cloudflare Pro...
echo 👨‍💻 Created by @bukanaol
echo 🌐 Version: 2.0.0
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python version: %PYTHON_VERSION%

REM Check if requirements are installed
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

REM Install/upgrade requirements
echo 📦 Installing/upgrading requirements...
pip install -r requirements.txt --upgrade

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Starting bot for first-time setup...
    echo 📝 Bot will ask for configuration details...
    echo.
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

REM Start the bot
echo 🤖 Starting bot...
echo 📊 Logs will be saved to: bot.log
echo 💾 Backups will be saved to: backups/
echo.
echo 🔄 Bot is starting... Press Ctrl+C to stop
echo.

REM Run the bot
python botcf.py

echo.
echo 🛑 Bot stopped.
pause