#!/bin/bash

# Discord Music Bot with Hidden Defense System
# Deployment script

echo "🚀 Deploying Discord Music Bot with Hidden Defense System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if config.env exists
if [ ! -f "config.env" ]; then
    echo "⚠️  config.env not found. Please copy config.env.example to config.env and configure it."
    echo "📋 Copying config.env.example to config.env..."
    cp config.env.example config.env
    echo "✅ Please edit config.env with your credentials before running the bot."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backups
mkdir -p logs

# Set permissions
echo "🔐 Setting permissions..."
chmod +x run_bot.py
chmod +x start.bat

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit config.env with your credentials"
echo "2. Run: python run_bot.py"
echo "3. Or on Windows: start.bat"
echo ""
echo "🛡️ Defense system ready"
echo "🎵 Music system ready"
echo "📧 Email alerts configured"
echo "🔒 Protected users: by_bytes (automatic)"
