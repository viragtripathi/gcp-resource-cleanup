#!/bin/bash
set -e

echo "➡️ Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "➡️ Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete! Use 'source venv/bin/activate' to activate."
