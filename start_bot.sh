#!/bin/bash

# Bot Cloudflare Pro - Startup Script
# Created by @bukanaol

echo "🚀 Starting Bot Cloudflare Pro..."
echo "👨‍💻 Created by @bukanaol"
echo "🌐 Version: 2.0.0"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python version $PYTHON_VERSION is too old. Required: $REQUIRED_VERSION+"
    exit 1
fi

echo "✅ Python version: $PYTHON_VERSION"

# Check if requirements are installed
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Install/upgrade requirements
echo "📦 Installing/upgrading requirements..."
pip3 install -r requirements.txt --upgrade

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Starting bot for first-time setup..."
    echo "📝 Bot will ask for configuration details..."
    echo ""
fi

# Create logs directory if it doesn't exist
mkdir -p logs
mkdir -p backups

# Start the bot
echo "🤖 Starting bot..."
echo "📊 Logs will be saved to: bot.log"
echo "💾 Backups will be saved to: backups/"
echo ""
echo "🔄 Bot is starting... Press Ctrl+C to stop"
echo ""

# Run the bot
python3 botcf.py

echo ""
echo "🛑 Bot stopped."