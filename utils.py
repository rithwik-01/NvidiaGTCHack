"""
Utility Functions for ZeroFail AI
Risk classification and study session simulator
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import json


def classify_risk(score: float, threshold_good: float = 80.0,
                  threshold_medium: float = 60.0) -> str:
    """
    Classify a score into a risk level.

    Args:
        score: The score to classify (0-100)
        threshold_good: Score threshold for LOW risk (default: 80)
        threshold_medium: Score threshold for MEDIUM risk (default: 60)

    Returns:
        "HIGH", "MEDIUM", or "LOW" risk level
    """
    if score >= threshold_good:
        return "LOW"
    elif score >= threshold_medium:
        return "MEDIUM"
    else:
        return "HIGH"


def get_risk_color(risk_level: str) -> str:
    """Return color for risk level badge."""
    colors = {
        "HIGH": "#ef4444",    # red
        "MEDIUM": "#f59e0b",  # yellow/amber
        "LOW": "#22c55e"      # green
    }
    return colors.get(risk_level.upper(), "#6b7280")


def simulate_study_session(assignments: List[Dict[str, Any]],
                            available_hours: int = 15) -> Dict[str, Any]:
    """
    Simulate an optimal study session schedule based on assignment priorities.

    Args:
        assignments: List of assignment dicts with name, points, due_date
        available_hours: Total hours available for study session

    Returns:
        Dict with scheduled study blocks and recommendations
    """
    # Sort assignments by due date
    sorted_assignments = sorted(assignments, key=lambda x: x['due_date'])

    # Calculate time allocation based on points and urgency
    total_points = sum(a['points'] for a in sorted_assignments)

    schedule = {
        "total_hours": available_hours,
        "sessions": [],
        "recommendations": []
    }

    today = datetime.now()
    hours_remaining = available_hours

    for i, assignment in enumerate(sorted_assignments):
        if hours_remaining <= 0:
            break

        due_date = datetime.strptime(assignment['due_date'], "%Y-%m-%d")
        days_until = (due_date - today).days

        # Prioritize: closer due date + higher points
        urgency_factor = max(1, 7 - days_until)  # Higher = more urgent
        point_weight = assignment['points'] / total_points

        # Calculate hours for this assignment
        hours = min(
            hours_remaining,
            round((urgency_factor * point_weight * available_hours * 2), 1)
        )
        hours = max(1, hours)  # At least 1 hour

        hours_remaining -= hours

        schedule["sessions"].append({
            "assignment": assignment['name'],
            "duration_hours": hours,
            "due_in_days": days_until,
            "priority": "HIGH" if days_until < 7 else "MEDIUM" if days_until < 14 else "LOW"
        })

    # Generate recommendations
    if any(a['category'] == 'quizzes' and classify_risk(a.get('current_score', 0)) == 'HIGH'
           for a in assignments if 'category' in a):
        schedule["recommendations"].append(
            "⚠️ Focus extra time on quiz review materials"
        )

    if len(sorted_assignments) > 0:
        first_assignment = sorted_assignments[0]
        due_date = datetime.strptime(first_assignment['due_date'], "%Y-%m-%d")
        days_until = (due_date - today).days
        schedule["recommendations"].append(
            f"📚 Start with {first_assignment['name']} - due in {days_until} days"
        )

    schedule["recommendations"].append(
        "💡 Take 5-minute breaks every hour for better retention"
    )

    return schedule


def format_json_safe(obj: Any) -> str:
    """
    Safely convert an object to JSON string.

    Args:
        obj: Object to serialize

    Returns:
        JSON string or error message
    """
    try:
        return json.dumps(obj, indent=2, default=str)
    except Exception as e:
        return f"Error serializing: {str(e)}"


def parse_semester_range(sem_start: str, sem_end: str) -> tuple[datetime, datetime]:
    """
    Parse semester date strings into datetime objects.

    Args:
        sem_start: Start date string (YYYY-MM-DD)
        sem_end: End date string (YYYY-MM-DD)

    Returns:
        Tuple of (start_date, end_date) as datetime objects
    """
    return (
        datetime.strptime(sem_start, "%Y-%m-%d"),
        datetime.strptime(sem_end, "%Y-%m-%d")
    )


def calculate_current_grade(grading_schema: Dict[str, Any]) -> float:
    """
    Calculate current grade based on grading schema.

    Args:
        grading_schema: Dict with categories, weights, and current scores

    Returns:
        Current grade percentage (0-100)
    """
    total_weighted_score = 0.0
    total_weight_used = 0.0

    for cat, info in grading_schema['categories'].items():
        current_score = info.get('current_score')
        if current_score is not None:
            total_weighted_score += current_score * info['weight']
            total_weight_used += info['weight']

    if total_weight_used == 0:
        return 0.0

    return total_weighted_score / total_weight_used
