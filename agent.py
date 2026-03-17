"""
ZeroFail AI Agent Orchestrator
ReAct workflow for academic risk analysis
"""

from datetime import datetime
from typing import Dict, Any
import tools
from llm_calls import (
    knowledge_gap_forecast,
    tonight_study_optimizer,
    cascade_risk_analyzer
)


class ZeroFailAgent:
    """Academic agent that orchestrates LLM analysis via ReAct workflow."""

    def __init__(self):
        self.results = {}
        self.react_trace = []

    def _log_react(self, phase: str, action: str, observation: str) -> None:
        """
        Log a ReAct step to trace list.

        Args:
            phase: REASON, ACT, or OBSERVE
            action: What was done
            observation: What was observed
        """
        timestamp = datetime.now().isoformat()
        print(f"[{phase}] {action}")
        print(f"[OBSERVE] {observation}")
        self.react_trace.append({
            "phase": phase,
            "action": action,
            "observation": observation,
            "timestamp": timestamp
        })

    def run_agent(self) -> Dict[str, Any]:
        """
        Run complete ReAct workflow: 5 steps for academic risk analysis.

        Returns:
            Dict containing all analysis results and react trace
        """
        print("🚀 Starting ZeroFail AI agent...")

        # Step 1: Load course data to build student academic profile
        print("\n📚 Step 1: Loading course data to build student academic profile")
        self._log_react(
            "REASON",
            "Loading course data to build student academic profile",
            "Calling all 5 read tools"
        )

        try:
            syllabus_result = tools.read_syllabus_schedule()
            assignments_result = tools.get_assignments()
            grades_result = tools.get_current_grades()
            weights_result = tools.get_grade_weights()
            profile_result = tools.get_student_profile()

            syllabus = syllabus_result["output"]
            assignments = assignments_result["output"]
            grades = grades_result["output"]
            weights = weights_result["output"]
            profile = profile_result["output"]

            n_assignments = len(assignments)
            overall_grade = grades.get("overall", 0)
            failing_categories = [cat for cat, score in grades.items() if isinstance(score, (int, float)) and score < 60]

            self._log_react(
                "OBSERVE",
                f"Loaded {n_assignments} assignments. Student at {overall_grade}% overall. Failing: {', '.join(failing_categories) if failing_categories else 'none'}",
                "Student profile loaded successfully"
            )

            self.results['syllabus'] = syllabus
            self.results['assignments'] = assignments
            self.results['grades'] = grades
            self.results['weights'] = weights
            self.results['profile'] = profile
        except Exception as e:
            self._log_react(
                "OBSERVE",
                f"Error loading course data: {str(e)}",
                "Failed to load course data"
            )
            raise

        # Step 2: Identify knowledge gaps before they become failing grades
        print("\n📡 Step 2: Identifying knowledge gaps before they become failing grades")
        self._log_react(
            "REASON",
            "Identifying knowledge gaps before they become failing grades",
            "Calling knowledge_gap_forecast()"
        )

        try:
            quiz_scores = grades.get("quiz_scores", [])
            weak_topics = profile.get("weak_topics", [])

            gap_forecast = knowledge_gap_forecast(quiz_scores, syllabus, weak_topics)

            if hasattr(gap_forecast, 'at_risk_weeks'):
                n_at_risk = len(gap_forecast.at_risk_weeks)
                highest_risk = gap_forecast.highest_risk_week
                self._log_react(
                    "OBSERVE",
                    f"{n_at_risk} at-risk weeks identified. Highest risk: {highest_risk}",
                    gap_forecast.summary
                )
            else:
                self._log_react(
                    "OBSERVE",
                    "Knowledge gap forecast unavailable due to API error",
                    "Unable to identify at-risk weeks"
                )

            self.results['gap_forecast'] = gap_forecast
        except Exception as e:
            self._log_react(
                "OBSERVE",
                f"Error forecasting knowledge gaps: {str(e)}",
                "Failed to identify knowledge gaps"
            )
            raise

        # Step 3: Build optimal study plan for tonight
        print("\n📅 Step 3: Building optimal study plan for tonight")
        self._log_react(
            "REASON",
            "Building optimal study plan for tonight given 3 available hours",
            "Calling tonight_study_optimizer()"
        )

        try:
            available_hours = profile.get("available_hours_tonight", 3)

            tonight_plan = tonight_study_optimizer(available_hours, assignments, grades, weak_topics)

            if hasattr(tonight_plan, 'tonight_plan'):
                first_slot = tonight_plan.tonight_plan[0] if tonight_plan.tonight_plan else None
                slot_summary = f"{first_slot.slot} – {first_slot.action}" if first_slot else "No slots"
                self._log_react(
                    "OBSERVE",
                    f"Plan generated: {slot_summary}. Expected impact: {tonight_plan.expected_impact}",
                    tonight_plan.expected_impact
                )
            else:
                self._log_react(
                    "OBSERVE",
                    "Tonight plan unavailable due to API error",
                    "Unable to generate study plan"
                )

            self.results['tonight_plan'] = tonight_plan
        except Exception as e:
            self._log_react(
                "OBSERVE",
                f"Error generating tonight's plan: {str(e)}",
                "Failed to build study plan"
            )
            raise

        # Step 4: Scan for second-order risks invisible in grade percentage
        print("\n⚡ Step 4: Scanning for second-order risks invisible in grade percentage")
        self._log_react(
            "REASON",
            "Scanning for second-order risks invisible in grade percentage",
            "Calling cascade_risk_analyzer()"
        )

        try:
            cascade_risks = cascade_risk_analyzer(assignments, grades, weights)

            if hasattr(cascade_risks, 'cascade_risks'):
                n_risks = len(cascade_risks.cascade_risks)
                critical_path = cascade_risks.critical_path
                self._log_react(
                    "OBSERVE",
                    f"{n_risks} cascade risks found. Critical path: {critical_path}",
                    cascade_risks.invisible_to_canvas
                )
            else:
                self._log_react(
                    "OBSERVE",
                    "Cascade risks unavailable due to API error",
                    "Unable to identify cascade risks"
                )

            self.results['cascade_risks'] = cascade_risks
        except Exception as e:
            self._log_react(
                "OBSERVE",
                f"Error analyzing cascade risks: {str(e)}",
                "Failed to identify cascade risks"
            )
            raise

        # Step 5: Execute highest-leverage autonomous action
        print("\n✅ Step 5: Executing highest-leverage autonomous action")
        self._log_react(
            "REASON",
            "Executing highest-leverage autonomous action",
            "Calling tools.block_study_session() for top priority item"
        )

        try:
            # Get top priority from tonight plan
            top_slot = None
            if hasattr(tonight_plan, 'tonight_plan') and tonight_plan.tonight_plan:
                top_slot = tonight_plan.tonight_plan[0]

            if top_slot:
                start_time = top_slot.slot.split('–')[0].strip()
                assignment_name = top_slot.assignment_or_topic
                duration = top_slot.duration_hours

                block_result = tools.block_study_session(assignment_name, start_time, duration)

                self._log_react(
                    "OBSERVE",
                    f"Study block confirmed: {assignment_name} {start_time} {duration}h",
                    block_result["output"]["message"]
                )

                self.results['study_block_confirmed'] = block_result["output"]
            else:
                self._log_react(
                    "OBSERVE",
                    "No study session to confirm - no slots in tonight plan",
                    "Unable to confirm study block"
                )

                self.results['study_block_confirmed'] = None
        except Exception as e:
            self._log_react(
                "OBSERVE",
                f"Error confirming study block: {str(e)}",
                "Failed to confirm study block"
            )
            raise

        # Calculate overall risk
        overall_grade = grades.get("overall", 0)
        if overall_grade >= 70:
            overall_risk = "LOW"
        elif overall_grade >= 60:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "HIGH"

        print(f"\n🎯 Agent complete! Overall risk: {overall_risk}")

        return {
            'gap_forecast': self.results['gap_forecast'],
            'tonight_plan': self.results['tonight_plan'],
            'cascade_risks': self.results['cascade_risks'],
            'study_block_confirmed': self.results['study_block_confirmed'],
            'react_trace': self.react_trace,
            'overall_risk': overall_risk
        }


def run_what_if(skip_assignment: str) -> Dict[str, Any]:
    """
    Run cascade risk analyzer with an assignment removed for what-if analysis.

    Args:
        skip_assignment: Name of assignment to skip (e.g., "Workbook 2")

    Returns:
        Dict with cascade risks for the what-if scenario
    """
    print(f"🔀 Running what-if analysis: Skip {skip_assignment}")

    # Load data
    assignments = tools.get_assignments()["output"]
    grades = tools.get_current_grades()["output"]
    weights = tools.get_grade_weights()["output"]

    # Remove the specified assignment
    filtered_assignments = [a for a in assignments if a["name"] != skip_assignment]

    # Run cascade risk analyzer
    cascade_risks = cascade_risk_analyzer(filtered_assignments, grades, weights)

    return {
        'cascade_risks': cascade_risks,
        'skipped_assignment': skip_assignment,
        'scenario': f"What if {skip_assignment} is skipped?"
    }


if __name__ == "__main__":
    # Run agent in standalone mode for testing
    import json
    results = run_agent()
    print("\n" + "="*50)
    print("FINAL RESULTS:")
    print("="*50)
    print(json.dumps(results, indent=2, default=str))
