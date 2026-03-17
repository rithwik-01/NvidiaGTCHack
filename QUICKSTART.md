# Quick Start Guide - ZeroFail AI

## One-Time Setup (5 minutes)

### 1. Get API Key
```bash
# Visit https://openrouter.ai/keys and get your free API key
```

### 2. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your key:
# OPENROUTER_API_KEY=your_actual_key_here
```

### 3. Install Dependencies
```bash
# Run the setup script
./setup.sh

# Or manually:
pip install -r requirements.txt
cd frontend
npm install
```

## Running the Application

### Start Both Servers (Recommended)

**Terminal 1 - Backend:**
```bash
uvicorn server:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open in Browser:**
```
http://localhost:3000
```

### Or Use Legacy Streamlit UI

```bash
streamlit run app.py
# Opens at http://localhost:8501
```

## Using the Application

### Basic Flow
1. Click "▶ Run Agent" button
2. Watch the 5-step agent workflow execute
3. Review results in cards:
   - Knowledge Gap Forecast (weeks at risk)
   - Tonight's Study Plan (time-blocked)
   - Cascade Risks (second-order consequences)
   - Autonomous Action (confirmed study block)

### What-If Analysis
1. After initial run completes
2. Click "🔀 What-if: Skip Workbook 2?"
3. See how cascade risks change with that assignment removed

## Troubleshooting

**Problem: "API key not set" error**
```bash
# Check .env file exists and has key
cat .env
```

**Problem: "Connection refused" error**
```bash
# Make sure backend is running
curl http://localhost:8000
```

**Problem: Frontend won't start**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules .vite
npm install
```

## Architecture Overview

```
User clicks "Run Agent"
    ↓
React UI sends POST to /api/run-agent
    ↓
FastAPI server calls agent.run_agent()
    ↓
Python agent executes 5-step ReAct workflow
    ↓
LLM calls to NVIDIA Nemotron via OpenRouter
    ↓
Results returned as JSON
    ↓
React UI updates with animations
```

## Key Features

- **Real-time Agent Workflow**: Watch each step execute with live updates
- **Visual Timeline**: See tonight's study plan as a visual timeline
- **Risk Analysis**: Identify cascade risks before they become problems
- **What-If Scenarios**: Test "what if I skip this assignment?"
- **Dark Command Center Aesthetic**: Professional, space-inspired design
- **Responsive Design**: Works on desktop, tablet, and mobile

## Performance Tips

- Keep the backend running for faster subsequent runs
- The frontend has hot module replacement for instant updates
- Results are cached locally during a session

## Next Steps

1. Customize the mock data in `mock_data.py` for your courses
2. Add real Canvas API integration
3. Deploy to production (see IMPLEMENTATION.md for details)
4. Add more visualization types
5. Implement user authentication

## Support

For detailed implementation information, see `IMPLEMENTATION.md`
For project overview, see `README.md`
