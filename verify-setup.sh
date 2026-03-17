#!/bin/bash

echo "🔍 Verifying ZeroFail AI Setup..."

# Check Python files
echo "📄 Checking Python files..."
required_python_files=("server.py" "agent.py" "llm_calls.py" "tools.py" "mock_data.py" "utils.py")
for file in "${required_python_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING!"
    fi
done

# Check frontend files
echo "📄 Checking frontend files..."
required_frontend_files=(
    "package.json"
    "vite.config.ts"
    "tailwind.config.ts"
    "tsconfig.json"
    "index.html"
    "src/App.tsx"
    "src/main.tsx"
    "src/types/agent.ts"
    "src/hooks/useAgentRun.ts"
    "src/components/Nav.tsx"
    "src/components/HeroSection.tsx"
    "src/components/AgentStepper.tsx"
    "src/components/GapForecastCard.tsx"
    "src/components/StudyPlanCard.tsx"
    "src/components/CascadeRisksCard.tsx"
    "src/components/ActionCard.tsx"
)

for file in "${required_frontend_files[@]}"; do
    if [ -f "frontend/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING!"
    fi
done

# Check documentation
echo "📄 Checking documentation..."
required_docs=("README.md" "QUICKSTART.md" "IMPLEMENTATION.md")
for file in "${required_docs[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING!"
    fi
done

# Check .env
echo "🔐 Checking environment..."
if [ -f ".env" ]; then
    echo "  ✅ .env file exists"
    if grep -q "OPENROUTER_API_KEY" .env; then
        echo "  ✅ OPENROUTER_API_KEY is set"
    else
        echo "  ⚠️  OPENROUTER_API_KEY not found in .env"
    fi
else
    echo "  ❌ .env file - MISSING! Run: cp .env.example .env"
fi

# Check Python dependencies
echo "🐍 Checking Python dependencies..."
if command -v python3 &> /dev/null; then
    echo "  ✅ Python 3 installed"
    if python3 -c "import fastapi" 2>/dev/null; then
        echo "  ✅ FastAPI installed"
    else
        echo "  ⚠️  FastAPI not installed - Run: pip install -r requirements.txt"
    fi
else
    echo "  ❌ Python 3 not found"
fi

# Check Node.js and npm
echo "📦 Checking Node.js dependencies..."
if command -v node &> /dev/null; then
    echo "  ✅ Node.js installed"
    if command -v npm &> /dev/null; then
        echo "  ✅ npm installed"
        if [ -d "frontend/node_modules" ]; then
            echo "  ✅ node_modules exists"
        else
            echo "  ⚠️  node_modules not found - Run: cd frontend && npm install"
        fi
    else
        echo "  ❌ npm not found"
    fi
else
    echo "  ❌ Node.js not found"
fi

echo ""
echo "✅ Verification complete!"
echo ""
echo "Next steps:"
echo "1. If any ❌ above, fix those issues first"
echo "2. Start backend: uvicorn server:app --reload --port 8000"
echo "3. Start frontend: cd frontend && npm run dev"
echo "4. Open: http://localhost:3000"
