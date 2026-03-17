"""
LLM Calls for ZeroFail AI
All calls use NVIDIA Nemotron via OpenRouter
"""

import os
import json
import re
from typing import List, Dict, Any
from openai import OpenAI
from pydantic import BaseModel, Field


# Pydantic models for response validation
class AtRiskWeek(BaseModel):
    week: int
    date: str
    topic: str
    risk_level: str  # HIGH, MEDIUM, LOW
    reason: str
    prerequisite_gap: str
    recommended_prep: str
    prep_hours_needed: float


class GapForecastResponse(BaseModel):
    at_risk_weeks: List[AtRiskWeek]
    highest_risk_week: str
    summary: str


class TonightSlot(BaseModel):
    slot: str  # e.g., '6:00 PM – 7:30 PM'
    assignment_or_topic: str
    action: str
    duration_hours: float
    leverage_reason: str


class SkippedItem(BaseModel):
    name: str
    reason: str


class TonightPlanResponse(BaseModel):
    tonight_plan: List[TonightSlot]
    skipped: List[SkippedItem]
    expected_impact: str


class CascadeRisk(BaseModel):
    trigger: str
    consequence: str
    affected_assignments: List[str]
    severity: str  # HIGH, MEDIUM, LOW
    time_to_impact: str  # e.g., '3 weeks'
    action_now: str


class CascadeRisksResponse(BaseModel):
    cascade_risks: List[CascadeRisk]
    critical_path: str
    invisible_to_canvas: str


# Model name via OpenRouter
MODEL = "nvidia/nemotron-3-nano-30b-a3b"

# Required headers for OpenRouter
EXTRA_HEADERS = {
    "HTTP-Referer": "https://zerofail-ai",
    "X-Title": "ZeroFail AI"
}


def _get_client():
    """
    Get OpenAI client for OpenRouter (lazy initialization).

    Returns:
        OpenAI client instance
    """
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY", ""),
    )


def _strip_markdown_fences(content: str) -> str:
    """
    Strip markdown code fences from LLM response.

    Args:
        content: Raw LLM response

    Returns:
        Cleaned JSON string
    """
    # Remove ```json or ``` fences
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'```\s*', '', content)
    return content.strip()


def call_nemotron(function_name: str, system_prompt: str, user_prompt: str, response_model: type[BaseModel]) -> BaseModel:
    """
    Make a call to NVIDIA Nemotron via OpenRouter.

    Args:
        function_name: Name of the function being called (for logging)
        system_prompt: System instruction for the model
        user_prompt: User query/content
        response_model: Pydantic model for response validation

    Returns:
        Validated response object matching response_model
    """
    print(f"[LLM] {function_name} → called")

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            extra_headers=EXTRA_HEADERS,
            temperature=0.3,
        )

        content = response.choices[0].message.content
        print(f"[LLM] {function_name} → RAW RESPONSE:\n{content[:500]}...")  # Debug: Print first 500 chars
        content = _strip_markdown_fences(content)
        print(f"[LLM] {function_name} → AFTER STRIP:\n{content[:500]}...")  # Debug: Print first 500 chars
        return response_model.model_validate_json(content)
    except Exception as e:
        print(f"[LLM] {function_name} → error: {str(e)}")
        # Return safe fallback dict
        return _get_fallback_response(function_name)


def _get_fallback_response(function_name: str) -> BaseModel:
    """Get a safe fallback response for error cases."""
    if function_name == "knowledge_gap_forecast":
        return GapForecastResponse(
            at_risk_weeks=[],
            highest_risk_week="Unknown",
            summary="Unable to analyze due to API error"
        )
    elif function_name == "tonight_study_optimizer":
        return TonightPlanResponse(
            tonight_plan=[],
            skipped=[],
            expected_impact="Unable to generate plan due to API error"
        )
    elif function_name == "cascade_risk_analyzer":
        return CascadeRisksResponse(
            cascade_risks=[],
            critical_path="Unknown",
            invisible_to_canvas="Unable to analyze due to API error"
        )
    return None


def knowledge_gap_forecast(quiz_scores: List[Dict[str, Any]], syllabus_schedule: List[Dict[str, Any]], weak_topics: List[str]) -> GapForecastResponse:
    """
    Cross-reference student past quiz scores against upcoming syllabus topics.
    Identify which future weeks student is likely to struggle in BEFORE they arrive.

    Args:
        quiz_scores: List of past quiz scores with topic and score
        syllabus_schedule: List of upcoming weekly topics
        weak_topics: List of topics student struggles with

    Returns:
        GapForecastResponse with at-risk weeks and recommendations
    """
    system_prompt = """You are an academic risk analyst. Cross-reference student past quiz scores against upcoming syllabus topics. Identify which future weeks student is likely to struggle in BEFORE they arrive, based on prerequisite knowledge gaps.

Analyze the quiz scores, syllabus topics, and weak topics. Look for:
1. Weeks covering topics the student has struggled with before
2. Topics that depend on the student's weak areas
3. Sequencing issues where knowledge gaps compound

Return a JSON object with this exact structure:
{
    "at_risk_weeks": [
        {
            "week": 1,
            "date": "2026-XX-XX",
            "topic": "topic name",
            "risk_level": "HIGH| MEDIUM| LOW",
            "reason": "why past scores predict struggle here",
            "prerequisite_gap": "specific knowledge missing",
            "recommended_prep": "concrete action before that week",
            "prep_hours_needed": 0.0
        }
    ],
    "highest_risk_week": "Week X - topic",
    "summary": "one-sentence summary of forecast"
}

Be specific about prerequisites and concrete about preparation actions. Sort at_risk_weeks by risk_level (HIGH first)."""

    user_prompt = f"""Past Quiz Scores:
{json.dumps(quiz_scores, indent=2)}

Upcoming Syllabus Schedule:
{json.dumps(syllabus_schedule, indent=2)}

Student's Weak Topics:
{', '.join(weak_topics)}

Please identify which future weeks the student is at risk of struggling in."""

    return call_nemotron("knowledge_gap_forecast", system_prompt, user_prompt, GapForecastResponse)


def tonight_study_optimizer(available_hours: float, assignments: List[Dict[str, Any]], current_grades: Dict[str, Any], weak_topics: List[str]) -> TonightPlanResponse:
    """
    Generate a specific time-blocked plan for tonight.
    Prioritize high-leverage work where effort now prevents larger future pain.

    Args:
        available_hours: Hours available tonight (typically 3)
        assignments: List of pending assignments with estimated hours
        current_grades: Current grades by category
        weak_topics: Topics student struggles with

    Returns:
        TonightPlanResponse with time-blocked schedule
    """
    system_prompt = """You are a time-allocation strategist. Given student available hours tonight, all pending assignments with effort estimates, and their weak topics, produce a specific time-blocked plan for tonight. Reason about sequence and duration.

Prioritize high-leverage work:
1. Assignments where effort now prevents larger future pain
2. Quizzes on weak topics (immediate grade boost)
3. Group projects requiring coordination
4. Early-stage work on large solo projects

Return a JSON object with this exact structure:
{
    "tonight_plan": [
        {
            "slot": "6:00 PM – 7:30 PM",
            "assignment_or_topic": "Quiz 2 review",
            "action": "specific action not vague advice",
            "duration_hours": 1.5,
            "leverage_reason": "why this slot maximizes grade impact"
        }
    ],
    "skipped": [
        {
            "name": "assignment name",
            "reason": "why deprioritized"
        }
    ],
    "expected_impact": "one-sentence impact statement"
}

Total time in tonight_plan must exactly match available_hours. Make actions specific, not vague advice."""

    user_prompt = f"""Available Hours Tonight: {available_hours}

Pending Assignments:
{json.dumps(assignments, indent=2)}

Current Grades:
{json.dumps(current_grades, indent=2)}

Student's Weak Topics:
{', '.join(weak_topics)}

Please produce a specific time-blocked study plan for tonight."""

    return call_nemotron("tonight_study_optimizer", system_prompt, user_prompt, TonightPlanResponse)


def cascade_risk_analyzer(assignments: List[Dict[str, Any]], current_grades: Dict[str, Any], grade_weights: Dict[str, Any]) -> CascadeRisksResponse:
    """
    Identify second-order consequences invisible in current grade percentage.
    Focus on group coordination, feed-through risks, cumulative failures.

    Args:
        assignments: All assignments with submission_type and estimated_hours
        current_grades: Current grades by category
        grade_weights: Grade weights by category

    Returns:
        CascadeRisksResponse with cascade risks and critical path
    """
    system_prompt = """You are a second-order consequences analyst. Identify risks that are NOT visible in the current grade percentage. Focus on issues that cascade.

Look for:
1. Group project coordination lag (if group assignment is late, what depends on it?)
2. Assignments that feed into later high-weight deliverables
3. Cumulative category failures (if failing quizzes, does it impact final exam?)
4. Time compression risks (multiple large assignments due close together)

Do NOT repeat what Canvas already shows (current grade, what's due). Focus on invisible risks.

Return a JSON object with this exact structure:
{
    "cascade_risks": [
        {
            "trigger": "root cause",
            "consequence": "what actually breaks downstream",
            "affected_assignments": ["assignment1", "assignment2"],
            "severity": "HIGH| MEDIUM| LOW",
            "time_to_impact": "3 weeks",
            "action_now": "what to do today to prevent it"
        }
    ],
    "critical_path": "single most important thing to protect",
    "invisible_to_canvas": "one-liner on what Canvas misses here"
}

Be specific about triggers and concrete about actions. Sort cascade_risks by severity (HIGH first)."""

    user_prompt = f"""All Assignments:
{json.dumps(assignments, indent=2)}

Current Grades:
{json.dumps(current_grades, indent=2)}

Grade Weights:
{json.dumps(grade_weights, indent=2)}

Please identify second-order cascade risks invisible to Canvas."""

    return call_nemotron("cascade_risk_analyzer", system_prompt, user_prompt, CascadeRisksResponse)
