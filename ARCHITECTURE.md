# ZeroFail AI Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                               │
│  React SPA (localhost:3000) - Dark Command Center Aesthetic         │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API LAYER                                      │
│  FastAPI Server (localhost:8000)                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Endpoints:                                                 │   │
│  │  GET  /                    - Health check                   │   │
│  │  POST /api/run-agent       - Run complete workflow         │   │
│  │  POST /api/whatif          - What-if analysis              │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ Python
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATOR                               │
│  ZeroFailAgent - ReAct Workflow                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 5-Step Workflow:                                            │   │
│  │  1. Load Data        → Tools (syllabus, grades, etc.)      │   │
│  │  2. Gap Forecast     → Knowledge Gap Agent                   │   │
│  │  3. Study Plan       → Tonight Optimizer Agent               │   │
│  │  4. Cascade Risks    → Risk Analyzer Agent                   │   │
│  │  5. Execute Action   → Study Block Tool                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ LLM API Calls
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      LLM PROVIDER                                    │
│  NVIDIA Llama 3.1 Nemotron-70B Instruct (via OpenRouter)            │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 3 Specialized Agents:                                         │   │
│  │  • Knowledge Gap Forecast Agent                               │   │
│  │  • Tonight Study Optimizer Agent                              │   │
│  │  • Cascade Risk Analyzer Agent                                │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend (React SPA)

```
App.tsx (Root Component)
├── Nav.tsx (Navigation Bar)
├── HeroSection.tsx (Main Call to Action)
│   └── StatPill.tsx (Summary Metrics)
├── AgentStepper.tsx (5-Step Workflow Visualization)
├── GapForecastCard.tsx (Knowledge Gaps)
│   └── RiskBadge.tsx (Risk Level Indicators)
├── StudyPlanCard.tsx (Tonight's Plan)
│   └── StudyPlanTimeline.tsx (Visual Timeline)
├── CascadeRisksCard.tsx (Second-Order Risks)
│   └── CascadeRisksStack.tsx (Risk Cards)
├── ActionCard.tsx (Confirmed Action)
│   └── DonutChart.tsx (Grade Breakdown)
└── SkeletonCard.tsx (Loading State)
```

### Data Flow

```
User Interaction
    ↓
React Component State Update
    ↓
useAgentRun Hook
    ↓
HTTP Request (fetch)
    ↓
FastAPI Endpoint
    ↓
Agent Orchestrator
    ↓
LLM API Calls (OpenRouter)
    ↓
Response Processing
    ↓
Pydantic Validation
    ↓
JSON Serialization
    ↓
HTTP Response
    ↓
React State Update
    ↓
UI Re-render with Animations
```

### State Management

```
Global State (useAgentRun Hook)
├── uiState: 'idle' | 'running' | 'complete' | 'error'
├── results: AgentResults | null
├── whatIfResults: WhatIfResults | null
├── error: string | null
├── currentStep: number (0-5)
├── runAgent(): Function
└── runWhatIf(): Function

Component Local State
├── hover states
├── expanded states
├── form inputs (if any)
└── modal states (if any)
```

## Data Models

### Python (Backend)

```
Pydantic Models:
├── AtRiskWeek
│   ├── week: int
│   ├── date: str
│   ├── topic: str
│   ├── risk_level: 'HIGH' | 'MEDIUM' | 'LOW'
│   ├── reason: str
│   ├── prerequisite_gap: str
│   ├── recommended_prep: str
│   └── prep_hours_needed: float
├── GapForecastResponse
│   ├── at_risk_weeks: List[AtRiskWeek]
│   ├── highest_risk_week: str
│   └── summary: str
├── TonightSlot
│   ├── slot: str (e.g., "6:00 PM – 7:30 PM")
│   ├── assignment_or_topic: str
│   ├── action: str
│   ├── duration_hours: float
│   └── leverage_reason: str
├── TonightPlanResponse
│   ├── tonight_plan: List[TonightSlot]
│   ├── skipped: List[SkippedItem]
│   └── expected_impact: str
├── CascadeRisk
│   ├── trigger: str
│   ├── consequence: str
│   ├── affected_assignments: List[str]
│   ├── severity: 'HIGH' | 'MEDIUM' | 'LOW'
│   ├── time_to_impact: str
│   └── action_now: str
└── CascadeRisksResponse
    ├── cascade_risks: List[CascadeRisk]
    ├── critical_path: str
    └── invisible_to_canvas: str
```

### TypeScript (Frontend)

```
Interface Definitions (types/agent.ts):
├── RiskLevel: 'HIGH' | 'MEDIUM' | 'LOW'
├── Phase: 'REASON' | 'ACT' | 'OBSERVE'
├── ReactTrace
│   ├── phase: Phase
│   ├── action: string
│   ├── observation: string
│   └── timestamp: string
├── AtRiskWeek
├── GapForecast
├── TonightSlot
├── TonightPlan
├── CascadeRisk
├── CascadeRisks
├── StudyBlockConfirmed
├── AgentResults
├── WhatIfResults
└── UIState: 'idle' | 'running' | 'complete' | 'error'
```

## Design System

### Color Palette

```
Background Colors:
├── bg-base: #080C12      - Deepest background
├── bg-surface: #0F1520   - Card surfaces
└── bg-elevated: #162030  - Hover/active states

Accent Colors:
├── accent-red: #FF3B3B   - HIGH risk
├── accent-amber: #F59E0B - MEDIUM risk
├── accent-green: #10B981 - LOW risk
├── accent-blue: #3B82F6  - Primary action
└── accent-cyan: #06B6D4  - Data highlights

Text Colors:
├── text-primary: #F1F5F9 - Body text
└── text-muted: #64748B   - Secondary text

Border:
└── border: #1E293B       - Borders/dividers
```

### Typography

```
Font Families:
├── Space Grotesk (600-700) - Headings
├── Inter (400)            - Body text
└── JetBrains Mono         - Data/times

Sizing:
├── Text base: 1rem (16px)
├── Text lg: 1.125rem (18px)
├── Text xl: 1.25rem (20px)
├── Text 2xl: 1.5rem (24px)
├── Text 3xl: 1.875rem (30px)
└── Text 4xl: 2.25rem (36px)
```

### Spacing

```
Scale:
├── px-1: 4px
├── px-2: 8px
├── px-3: 12px
├── px-4: 16px
├── px-6: 24px
├── px-8: 32px
└── px-12: 48px
```

## Deployment Architecture

### Development

```
Developer Machine
├── Frontend: Vite Dev Server (localhost:3000)
│   └── Proxy → FastAPI Backend
└── Backend: Uvicorn (localhost:8000)
    └── Calls → OpenRouter API
```

### Production (Future)

```
Production Infrastructure
├── Frontend Hosting (Vercel/Netlify)
│   └── Static Files from npm run build
├── Backend Hosting (Render/Railway/Heroku)
│   └── FastAPI + Uvicorn
└── API Provider
    └── OpenRouter → NVIDIA Nemotron
```

## Security Considerations

### Current Implementation
- API keys stored in environment variables (.env)
- CORS restricted to localhost:3000
- Input validation via Pydantic
- Error handling without sensitive data exposure

### Future Enhancements
- User authentication (JWT tokens)
- Rate limiting
- HTTPS only
- API key encryption at rest
- Input sanitization
- CSRF protection
- Content Security Policy

## Performance Optimization

### Current Optimizations
- Vite for fast development builds
- Tree-shaking for production
- Lazy component loading (ready to implement)
- Efficient re-renders with React state
- Code splitting via dynamic imports (ready to implement)

### Monitoring (Future)
- Lighthouse CI
- Web Vitals tracking
- Error tracking (Sentry)
- Performance monitoring
- User analytics

## Testing Strategy (Future)

### Unit Tests
- React component tests (Vitest + React Testing Library)
- Custom hook tests
- Utility function tests
- Type validation tests

### Integration Tests
- API endpoint tests
- Agent workflow tests
- End-to-end user flows (Playwright/Cypress)

### E2E Tests
- Critical user paths
- Cross-browser testing
- Mobile responsiveness
