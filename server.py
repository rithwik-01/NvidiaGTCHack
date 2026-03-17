"""
FastAPI Server for ZeroFail AI
Provides REST API endpoints for React frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agent import ZeroFailAgent, run_what_if
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env file
load_dotenv()


app = FastAPI(
    title="ZeroFail AI API",
    description="Forward-Looking Academic Risk Engine",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunAgentRequest(BaseModel):
    """Request body for running agent"""
    pass


class WhatIfRequest(BaseModel):
    """Request body for what-if analysis"""
    skip_assignment: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "ZeroFail AI API is running",
        "version": "1.0.0"
    }


@app.post("/api/run-agent")
async def run_agent_endpoint(request: RunAgentRequest):
    """
    Run the complete ZeroFail AI agent workflow.

    Returns:
        Dict with all analysis results:
        - gap_forecast: Knowledge gap forecast
        - tonight_plan: Tonight's study plan
        - cascade_risks: Cascade risk analysis
        - study_block_confirmed: Confirmed study block
        - react_trace: ReAct workflow trace
        - overall_risk: Overall risk level
    """
    try:
        agent = ZeroFailAgent()
        results = agent.run_agent()

        # Convert Pydantic models to dicts for JSON serialization
        response = {
            "gap_forecast": _pydantic_to_dict(results['gap_forecast']),
            "tonight_plan": _pydantic_to_dict(results['tonight_plan']),
            "cascade_risks": _pydantic_to_dict(results['cascade_risks']),
            "study_block_confirmed": results['study_block_confirmed'],
            "react_trace": results['react_trace'],
            "overall_risk": results['overall_risk']
        }

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running agent: {str(e)}"
        )


@app.post("/api/whatif")
async def what_if_endpoint(request: WhatIfRequest):
    """
    Run cascade risk analysis with an assignment removed.

    Args:
        skip_assignment: Name of assignment to skip (e.g., "Workbook 2")

    Returns:
        Dict with cascade risks for the what-if scenario
    """
    try:
        results = run_what_if(request.skip_assignment)

        # Convert Pydantic models to dicts
        response = {
            "cascade_risks": _pydantic_to_dict(results['cascade_risks']),
            "skipped_assignment": results['skipped_assignment'],
            "scenario": results['scenario']
        }

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running what-if analysis: {str(e)}"
        )


def _pydantic_to_dict(obj):
    """
    Convert Pydantic model to dict recursively.

    Args:
        obj: Pydantic model or dict

    Returns:
        Dict representation of the object
    """
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    elif isinstance(obj, dict):
        return {k: _pydantic_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_pydantic_to_dict(item) for item in obj]
    else:
        return obj


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
