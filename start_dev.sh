#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Development Environment Setup..."

# 1. Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install Python 3.8+."
    exit 1
fi

# 2. Create a virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 3. Check if virtual environment directory exists
if [ ! -d "venv/bin" ]; then
    echo "❌ Virtual environment directory not found!"
    exit 1
fi

# 4. Activate the virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated."
else
    echo "❌ Activation script not found!"
    exit 1
fi

# 5. Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# 6. Install requirements
if [ -f "./requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r ./requirements.txt
else
    echo "❗ ./requirements.txt not found!"
    exit 1
fi

# 7. Set PYTHONPATH
export PYTHONPATH=$(pwd)

# 8. Launch the FastAPI app
echo "🚀 Launching FastAPI app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Deactivate the virtual environment after closing the app
deactivate
