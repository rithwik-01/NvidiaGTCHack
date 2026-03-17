# ZeroFail AI - Deployment Guide

This guide covers deploying ZeroFail AI to Vercel while maintaining local development setup.

## Local Development

### Backend Setup

1. Create `.env` file in the project root (zerofail-ai/):
   ```bash
   # zerofail-ai/.env
   OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here
   ```

2. Start backend server:
   ```bash
   python3 -m uvicorn server:app --reload --port 8000
   ```

3. Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. Create `.env` file in frontend directory (zerofail-ai/frontend/):
   ```bash
   # zerofail-ai/frontend/.env
   VITE_API_URL=http://localhost:8000
   ```

2. Install dependencies (if not already installed):
   ```bash
   cd frontend
   npm install
   ```

3. Start frontend dev server:
   ```bash
   npm run dev
   ```

4. Frontend will be available at: `http://localhost:3000`

## Vercel Deployment

### Backend Deployment

1. **Push code to GitHub** (already done):
   - Repository: https://github.com/rithwik-01/NvidiaGTCHack

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import the GitHub repository: `rithwik-01/NvidiaGTCHack`
   - Vercel will detect Python runtime automatically

3. **Add Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add the following variable:
     ```
     OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here
     ```

4. **Backend will be deployed** at a URL like:
   - `https://zerofail-ai-backend.vercel.app` (or similar)

### Frontend Deployment

1. **Push code to GitHub** (already done):
   - Repository: https://github.com/rithwik-01/NvidiaGTCHack

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import the GitHub repository: `rithwik-01/NvidiaGTCHack`
   - Set **Root Directory** to: `frontend`
   - Vercel will detect the React/Vite setup automatically

3. **Add Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add the following variable:
     ```
     VITE_API_URL=https://your-backend-url.vercel.app
     ```
   - Replace `your-backend-url.vercel.app` with your actual deployed backend URL

4. **Frontend will be deployed** at a URL like:
   - `https://zerofail-ai.vercel.app` (or similar)

## How Deployment Works

### Backend (FastAPI on Vercel)

- `vercel.json` configures Python runtime
- `api.py` imports and exposes the FastAPI app from server.py
- `requirements.txt` lists Python dependencies
- OpenRouter API key is injected via environment variable

### Frontend (React + Vite on Vercel)

- `frontend/vercel.json` configures SPA routing (rewrites all routes to index.html)
- `frontend/src/hooks/useAgentRun.ts` uses `VITE_API_URL` for API calls
- Defaults to `/api` (proxy) for local development
- Uses deployed backend URL in production

## Verification

After deployment:

1. **Backend**: Visit `https://your-backend-url.vercel.app` and check:
   - `{"status": "ok", "message": "ZeroFail AI API is running"}`

2. **Frontend**: Visit `https://your-frontend-url.vercel.app` and:
   - Click "▶ Run Agent"
   - Verify results display correctly
   - Check browser console for API errors

## Troubleshooting

### Frontend API Errors

If you see "HTTP error! status: 500" or connection errors:

1. Check `VITE_API_URL` environment variable in Vercel dashboard
2. Verify backend URL is correct (no typos)
3. Check backend is deployed and responding (test root endpoint)

### Environment Variable Issues

Vite variables must start with `VITE_` to be available in the browser:
- ✅ `VITE_API_URL=https://api.example.com`
- ❌ `API_URL=https://api.example.com`

### Backend 404 Errors

If API endpoints return 404 on Vercel:

1. Verify `vercel.json` routes configuration
2. Check `api/index.py` exists and exports `app`
3. Ensure `requirements.txt` includes all dependencies

## Security Notes

- **Never commit `.env` files** to the repository
- Use `.env.example` as a template
- Store secrets in Vercel Environment Variables
- API keys are injected at runtime, not in code
