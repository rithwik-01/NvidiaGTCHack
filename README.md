# ZeroFail AI

Forward-Looking Academic Risk Engine for CMPE 280 Spring 2026 at San Jose State University.

---

## What It Does

ZeroFail AI answers three questions Canvas cannot:

- 🔮 **Which future weeks will I struggle in before they arrive?** — Cross-references past quiz performance against upcoming syllabus topics to identify prerequisite knowledge gaps before they cause failures
- ⏰ **How should I spend my next 3 hours to maximize my grade?** — Generates a specific time-blocked study plan prioritizing high-leverage work that prevents larger future pain
- ⚡ **What second-order consequences am I not seeing?** — Identifies cascade risks invisible in current grade percentage (group coordination lag, cumulative failures, feed-through risks)

---

## Why Nemotron?

ZeroFail AI uses **NVIDIA Llama 3.1 Nemotron-70B Instruct** via OpenRouter for its core intelligence:

1. **Structured Output** — Pydantic-validated JSON responses ensure reliable, parseable results for all three specialized agents
2. **Reasoning Over Unstructured Inputs** — 70B parameters enable deep analysis of syllabus topics, grade history, and student profile to surface non-obvious patterns
3. **Agentic Workflow Compatibility** — Strong instruction-following capabilities make it ideal for multi-step ReAct orchestration

---

## Architecture

```
Tools → Normalizer → 3 Nemotron Agents → ReAct Loop → FastAPI → React SPA
(mock)    (format)      (LLM calls)      (logging)      (API)      (UI)
```

**Component Breakdown:**

| Component | Purpose | Tech |
|-----------|---------|------|
| Tools | Mock Canvas API calls (syllabus, assignments, grades, profile) | Python |
| Normalizer | Format tool outputs for LLM consumption | Pydantic |
| Nemotron Agents | 3 specialized LLM calls (knowledge gaps, tonight optimizer, cascade risks) | OpenRouter API |
| ReAct Loop | REASON → ACT → OBSERVE trace with 5 steps | Custom |
| FastAPI Server | REST API endpoints for frontend | FastAPI + Uvicorn |
| React Frontend | Production-grade SPA with dark command-center aesthetic | React 18 + TypeScript + Tailwind CSS + Framer Motion |

---

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Get your OpenRouter API key at: https://openrouter.ai/keys

Set the `OPENROUTER_API_KEY` environment variable:

```bash
# macOS/Linux
export OPENROUTER_API_KEY=your_key_here

# Windows (PowerShell)
$env:OPENROUTER_API_KEY="your_key_here"

# Or create a .env file:
echo "OPENROUTER_API_KEY=your_key_here" > .env
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Run the Application

**Start the FastAPI backend:**
```bash
# From project root
uvicorn server:app --reload --port 8000
```

**Start the React frontend (in a new terminal):**
```bash
cd frontend
npm run dev
```

The UI will open at `http://localhost:3000`

---

### Legacy Streamlit UI (Optional)

The original Streamlit UI is still available:

```bash
streamlit run app.py
```

The Streamlit UI will open at `http://localhost:8501`

---

## Demo Flow

1. **Click "▶ Run Agent"** — The ReAct orchestrator executes 5 steps:
   - Loads course data and student profile
   - Analyzes knowledge gaps from past quiz scores
   - Generates tonight's time-blocked study plan
   - Identifies cascade risks invisible in grade
   - Confirms autonomous study block

2. **Review the Results** — 5 sections displayed:
   - 🧠 Agent Workflow Trace — Full ReAct loop with REASON/ACT/OBSERVE labels
   - 📡 Knowledge Gap Forecast — At-risk weeks with prerequisite gaps and prep actions
   - 📅 Tonight's Study Plan — Visual timeline of time blocks with specific actions
   - ⚡ Cascade Risks — Second-order consequences with trigger → consequence flow
   - ✅ Autonomous Action Confirmed — Study block confirmation with overall risk

3. **Try What-If Analysis** — Click "🔀 What-if: I skip Workbook 2?" to see cascade impact of skipping an assignment

---

## Project Structure

```
zerofail-ai/
├── .env.example          # API key template
├── .gitignore
├── README.md             # This file
├── server.py             # FastAPI server with REST API
├── app.py               # Legacy Streamlit UI (optional)
├── agent.py             # ReAct orchestrator (5 steps)
├── llm_calls.py         # 3 Nemotron LLM functions
├── mock_data.py         # CMPE 280 Spring 2026 mock data
├── requirements.txt      # Python dependencies
├── tools.py             # Mock tool functions
├── utils.py             # Helpers, risk classification
└── frontend/            # React SPA
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.ts
    ├── tsconfig.json
    └── src/
        ├── App.tsx
        ├── main.tsx
        ├── styles/
        │   └── globals.css
        ├── types/
        │   └── agent.ts
        ├── hooks/
        │   └── useAgentRun.ts
        └── components/
            ├── Nav.tsx
            ├── HeroSection.tsx
            ├── AgentStepper.tsx
            ├── GapForecastCard.tsx
            ├── StudyPlanCard.tsx
            ├── StudyPlanTimeline.tsx
            ├── CascadeRisksCard.tsx
            ├── CascadeRisksStack.tsx
            ├── ActionCard.tsx
            ├── DonutChart.tsx
            ├── RiskBadge.tsx
            └── SkeletonCard.tsx
```

---

## Tech Stack

**Backend:**
- **Server**: FastAPI + Uvicorn
- **LLM**: NVIDIA Llama 3.1 Nemotron-70B Instruct (via OpenRouter)
- **API Client**: OpenAI-compatible API client
- **Validation**: Pydantic 2.0+
- **Agentic Framework**: Custom ReAct orchestrator

**Frontend:**
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with custom dark theme
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Date Formatting**: date-fns
- **Typography**: Space Grotesk (headings), Inter (body), JetBrains Mono (data)
- **Build Tool**: Vite

---

## Hackathon Alignment

This project demonstrates:

- ✅ **Multi-step reasoning** over unstructured inputs (syllabus + grade history)
- ✅ **3 specialized Nemotron agents** with distinct roles (risk analyst, time strategist, consequences analyst)
- ✅ **ReAct workflow** visible in UI with full trace
- ✅ **Autonomous action** (study block confirmed via tools)
- ✅ **Real value Canvas cannot replicate** — forward-looking insights, not just reporting
- ✅ **NVIDIA Nemotron used for reasoning**, not content generation

---

## License

MIT License — Built for SJSU Hackathon 2026
