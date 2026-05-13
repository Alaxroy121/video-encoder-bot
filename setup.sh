#!/bin/bash

# Video Encoder Bot - Deployment Script

set -e

echo "🚀 Video Encoder Bot - Deployment Setup"
echo "========================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version"

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "❌ Please edit .env with your Telegram credentials:"
    echo "   - Get API_ID and API_HASH from https://my.telegram.org/apps"
    echo "   - Create a bot with @BotFather and get BOT_TOKEN"
    echo ""
    exit 1
fi

# Test setup
echo ""
echo "🔍 Testing setup..."
python3 test_setup.py

echo ""
echo "✅ Setup complete! Run 'python3 bot.py' to start the bot."
