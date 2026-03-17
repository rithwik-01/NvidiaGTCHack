"""
Mock Data for ZeroFail AI
CMPE 280 Spring 2026 — realistic and self-consistent with clear patterns
"""

SYLLABUS_SCHEDULE = [
    {
        "week": 1,
        "date": "2026-01-22",
        "topic": "UI/UX Principles + accessibility basics"
    },
    {
        "week": 3,
        "date": "2026-02-05",
        "topic": "Responsive Layouts — Flexbox and CSS Grid"
    },
    {
        "week": 6,
        "date": "2026-02-26",
        "topic": "React Basics with MUI — requires CSS Grid knowledge from Week 3"
    },
    {
        "week": 7,
        "date": "2026-03-05",
        "topic": "React Hooks + react-hook-form + zod — requires React Basics from Week 6"
    },
    {
        "week": 9,
        "date": "2026-03-19",
        "topic": "Figma tokens + accessible color palettes — requires Week 1 accessibility + Week 3 responsive design"
    },
    {
        "week": 10,
        "date": "2026-03-26",
        "topic": "WCAG accessibility audit — requires Week 1 accessibility + Week 9 accessible palettes"
    },
    {
        "week": 11,
        "date": "2026-04-02",
        "topic": "Ant Design comparison lab — requires React Hooks from Week 7 + component patterns"
    },
    {
        "week": 12,
        "date": "2026-04-09",
        "topic": "RAG-based UI integration — requires React Hooks from Week 7 + external API knowledge"
    },
    {
        "week": 14,
        "date": "2026-04-23",
        "topic": "Conversational UI + Prompt Engineering — requires Week 12 RAG integration"
    }
]


ASSIGNMENTS = [
    {
        "id": "quiz1",
        "name": "Quiz 1",
        "due_at": "2026-02-20T17:00:00Z",
        "points_possible": 50,
        "category": "quiz",
        "submission_type": "solo",
        "estimated_hours": 1.0,
        "description": "Tests knowledge from Weeks 1-3: UI/UX, responsive layouts"
    },
    {
        "id": "midterm_proposal",
        "name": "Midterm Proposal",
        "due_at": "2026-03-26T17:00:00Z",
        "points_possible": 100,
        "category": "midterm",
        "submission_type": "solo",
        "estimated_hours": 8.0,
        "description": "Submit proposal for final project direction"
    },
    {
        "id": "workbook2",
        "name": "Workbook 2",
        "due_at": "2026-04-09T17:00:00Z",
        "points_possible": 36,
        "category": "project",
        "submission_type": "group",
        "estimated_hours": 12.0,
        "description": "Build RAG-based UI integration with group"
    },
    {
        "id": "quiz2",
        "name": "Quiz 2",
        "due_at": "2026-04-11T17:00:00Z",
        "points_possible": 50,
        "category": "quiz",
        "submission_type": "solo",
        "estimated_hours": 1.0,
        "description": "Tests knowledge from Weeks 6-10: React, hooks, accessibility"
    },
    {
        "id": "final_project",
        "name": "Final Project",
        "due_at": "2026-05-07T17:00:00Z",
        "points_possible": 100,
        "category": "final",
        "submission_type": "solo",
        "estimated_hours": 40.0,
        "description": "Full conversational UI with prompt engineering (requires Week 14 knowledge)"
    }
]


GRADE_WEIGHTS = {
    "participation": 20,
    "midterm": 25,
    "final": 35,
    "quizzes": 20,
    "bonus": 5
}


CURRENT_GRADES = {
    "overall": 61.0,
    "participation": 85,
    "quizzes": 40,
    "midterm": None,
    "final": None,
    "quiz_scores": [
        {"week": 1, "topic": "UI/UX Principles", "score": 82, "max": 100},
        {"week": 3, "topic": "Responsive Layouts CSS", "score": 55, "max": 100},
        {"week": 6, "topic": "React Basics MUI", "score": 40, "max": 100},
        {"week": 7, "topic": "React Hooks Form Validation", "score": 35, "max": 100}
    ]
}


STUDENT_PROFILE = {
    "available_hours_tonight": 3,
    "strong_topics": ["UI/UX principles", "design thinking", "HTML semantics"],
    "weak_topics": ["React hooks", "zod validation", "CSS Grid advanced", "component state management"],
    "group_members_for_workbook": ["Alice", "Bob", "Carlos"],
    "last_group_sync": "2026-03-01"
}


FREE_SLOTS = [
    {"date": "2026-03-16", "day": "Monday", "time": "6:00 PM", "end_time": "7:30 PM", "hours": 1.5},
    {"date": "2026-03-16", "day": "Monday", "time": "8:00 PM", "end_time": "9:30 PM", "hours": 1.5},
    {"date": "2026-03-17", "day": "Tuesday", "time": "6:00 PM", "end_time": "7:30 PM", "hours": 1.5},
    {"date": "2026-03-17", "day": "Tuesday", "time": "8:00 PM", "end_time": "9:30 PM", "hours": 1.5},
    {"date": "2026-03-18", "day": "Wednesday", "time": "6:00 PM", "end_time": "7:30 PM", "hours": 1.5},
    {"date": "2026-03-22", "day": "Saturday", "time": "10:00 AM", "end_time": "4:00 PM", "hours": 6.0}
]
