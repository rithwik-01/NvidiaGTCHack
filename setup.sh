#!/bin/bash

echo "🚀 Setting up ZeroFail AI..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OPENROUTER_API_KEY"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Make sure OPENROUTER_API_KEY is set in .env"
echo "2. Start backend: uvicorn server:app --reload --port 8000"
echo "3. Start frontend: cd frontend && npm run dev"
echo "4. Open http://localhost:3000"
