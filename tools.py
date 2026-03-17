"""
Mock Tools for ZeroFail AI Agent
Simulates tool calls for agentic workflow
"""

from datetime import datetime
from typing import Dict, Any
from mock_data import (
    SYLLABUS_SCHEDULE,
    ASSIGNMENTS,
    CURRENT_GRADES,
    GRADE_WEIGHTS,
    STUDENT_PROFILE
)


def read_syllabus_schedule() -> Dict[str, Any]:
    """
    Read and return the course syllabus schedule.

    Returns:
        Dict with tool_name, input_params, output, timestamp
    """
    print(f"[TOOL] read_syllabus_schedule → OK")
    return {
        "tool_name": "read_syllabus_schedule",
        "input_params": {},
        "output": SYLLABUS_SCHEDULE,
        "timestamp": datetime.now().isoformat()
    }


def get_assignments() -> Dict[str, Any]:
    """
    Get list of course assignments.

    Returns:
        Dict with tool_name, input_params, output, timestamp
    """
    print(f"[TOOL] get_assignments → OK")
    return {
        "tool_name": "get_assignments",
        "input_params": {},
        "output": ASSIGNMENTS,
        "timestamp": datetime.now().isoformat()
    }


def get_current_grades() -> Dict[str, Any]:
    """
    Get current grades by category.

    Returns:
        Dict with tool_name, input_params, output, timestamp
    """
    print(f"[TOOL] get_current_grades → OK")
    return {
        "tool_name": "get_current_grades",
        "input_params": {},
        "output": CURRENT_GRADES,
        "timestamp": datetime.now().isoformat()
    }


def get_grade_weights() -> Dict[str, Any]:
    """
    Get grade weights by category.

    Returns:
        Dict with tool_name, input_params, output, timestamp
    """
    print(f"[TOOL] get_grade_weights → OK")
    return {
        "tool_name": "get_grade_weights",
        "input_params": {},
        "output": GRADE_WEIGHTS,
        "timestamp": datetime.now().isoformat()
    }


def get_student_profile() -> Dict[str, Any]:
    """
    Get student profile including strengths, weaknesses, availability.

    Returns:
        Dict with tool_name, input_params, output, timestamp
    """
    print(f"[TOOL] get_student_profile → OK")
    return {
        "tool_name": "get_student_profile",
        "input_params": {},
        "output": STUDENT_PROFILE,
        "timestamp": datetime.now().isoformat()
    }


def block_study_session(assignment_name: str, start_time: str, duration_hours: float) -> Dict[str, Any]:
    """
    Block a study session for an assignment.

    Args:
        assignment_name: Name of the assignment
        start_time: Start time for the study session
        duration_hours: Duration of the study session in hours

    Returns:
        Dict with tool_name, input_params, output, timestamp
    """
    print(f"[TOOL] block_study_session({assignment_name}, {start_time}, {duration_hours}) → OK")
    confirmation = {
        "assignment": assignment_name,
        "scheduled_start": start_time,
        "duration_hours": duration_hours,
        "status": "confirmed",
        "message": f"Study session for '{assignment_name}' blocked for {start_time} · {duration_hours}h · ✅ Confirmed"
    }
    return {
        "tool_name": "block_study_session",
        "input_params": {
            "assignment_name": assignment_name,
            "start_time": start_time,
            "duration_hours": duration_hours
        },
        "output": confirmation,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # Test all tools
    print("Testing ZeroFail AI Tools...")
    print("=" * 50)
    read_syllabus_schedule()
    get_assignments()
    get_current_grades()
    get_grade_weights()
    get_student_profile()
    block_study_session("Quiz 2", "7:00 PM", 1.5)
    print("=" * 50)
    print("All tools tested successfully!")
