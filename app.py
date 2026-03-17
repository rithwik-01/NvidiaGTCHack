"""
ZeroFail AI - Streamlit UI
Forward-Looking Academic Risk Engine for CMPE 280 Spring 2026
"""

import os
import streamlit as st
from dotenv import load_dotenv
from agent import ZeroFailAgent, run_what_if

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ZeroFail AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #10b981;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: bold;
        font-size: 0.875rem;
        color: white;
    }
    .risk-high { background: #ff4b4b; }
    .risk-medium { background: #ffa500; }
    .risk-low { background: #00c851; }
    .phase-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
        font-size: 0.75rem;
        margin-right: 0.5rem;
        background: #374151;
        color: #f3f4f6;
    }
    .card {
        background: #1c1f26;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #2d3748;
        margin-bottom: 1rem;
    }
    .timeline-block {
        background: #2d3748;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #10b981;
    }
    .cascade-card {
        background: #2d3748;
        padding: 1.25rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #f59e0b;
    }
    .at-risk-card {
        background: #2d3748;
        padding: 1.25rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #ef4444;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main Streamlit application."""

    # Header
    st.markdown('<h1 class="main-header">ZeroFail AI — Forward-Looking Academic Risk Engine</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by NVIDIA Nemotron · Sees what Canvas cannot</p>', unsafe_allow_html=True)

    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            placeholder="sk-or-v1-...",
            help="Enter your OpenRouter API key to use the AI agent"
        )
        st.caption("Get your key at: https://openrouter.ai/keys")
        st.divider()
        st.markdown("""
        **About ZeroFail AI**

        An AI-powered academic risk engine that:

        - 🔮 Predicts future struggles before they arrive
        - ⏰ Optimizes tonight's study time
        - ⚡ Reveals cascade risks invisible in grades

        Built for SJSU Hackathon 2026
        """)

    # Check for API key
    if not api_key and not os.getenv("OPENROUTER_API_KEY"):
        st.warning("⚠️ Please enter your OpenRouter API key in the sidebar to run the agent.")
        return

    # Set API key for this session
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key

    # Main action buttons
    st.divider()

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        run_button = st.button(
            "▶ Run Agent",
            type="primary",
            use_container_width=True,
            disabled=not api_key and not os.getenv("OPENROUTER_API_KEY")
        )

    # What-if button
    with col2:
        whatif_button = st.button(
            "🔀 What-if: I skip Workbook 2?",
            use_container_width=True,
            disabled=not api_key and not os.getenv("OPENROUTER_API_KEY")
        )

    # Store agent results in session state
    if "agent_results" not in st.session_state:
        st.session_state.agent_results = None
    if "whatif_results" not in st.session_state:
        st.session_state.whatif_results = None

    # Run main agent
    if run_button:
        with st.status("Running ZeroFail AI agent...", expanded=True) as status:
            try:
                agent = ZeroFailAgent()
                results = agent.run_agent()
                import sys
                print("="*50)
                print("[DEBUG] FULL RESULTS DICT:")
                print("="*50)
                import json
                print(json.dumps(results, indent=2, default=str))
                print("="*50)
                st.session_state.agent_results = results
                status.update(label="✅ Agent complete!", state="complete")

                # Stream react trace
                if results.get('react_trace'):
                    st.markdown("### 🧠 Agent Workflow Trace")
                    for trace in results['react_trace']:
                        phase = trace['phase']
                        action = trace['action']
                        observation = trace['observation']
                        phase_emoji = {"REASON": "🤔", "ACT": "⚡", "OBSERVE": "👁️"}.get(phase, "•")
                        st.markdown(f"""
                        <span class="phase-badge">{phase}</span> {phase_emoji} {action}
                        """, unsafe_allow_html=True)
                        st.caption(f"👁️ {observation}")
                        st.markdown("---")
            except Exception as e:
                st.error(f"❌ Error running agent: {str(e)}")
                st.session_state.agent_results = None

    # Run what-if analysis
    if whatif_button:
        with st.spinner("Running what-if analysis..."):
            try:
                results = run_what_if("Workbook 2")
                st.session_state.whatif_results = results
                st.success("✅ What-if analysis complete!")
            except Exception as e:
                st.error(f"❌ Error running what-if: {str(e)}")
                st.session_state.whatif_results = None

    # Display what-if results if available
    if st.session_state.whatif_results:
        st.divider()
        st.subheader("🔀 What-If Analysis: Skip Workbook 2")

        results = st.session_state.whatif_results
        cascade = results.get('cascade_risks', {})

        if hasattr(cascade, 'cascade_risks'):
            st.info(f"""
            **Scenario:** {results.get('scenario', 'What if Workbook 2 is skipped?')}

            **Critical Path:** {cascade.critical_path}

            **What Canvas Misses:** {cascade.invisible_to_canvas}
            """)

            st.markdown("### Cascade Risks")

            for risk in cascade.cascade_risks:
                severity_class = f"risk-{risk.severity.lower()}"
                st.markdown(f"""
                <div class="cascade-card">
                    <span class="risk-badge {severity_class}">{risk.severity}</span>
                    <strong>Trigger:</strong> {risk.trigger}
                    <br/>
                    <strong>Consequence:</strong> {risk.consequence}
                    <br/>
                    <strong>Affected:</strong> {', '.join(risk.affected_assignments)}
                    <br/>
                    <strong>Impact in:</strong> {risk.time_to_impact}
                    <br/>
                    <strong>Action Now:</strong> {risk.action_now}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Cascade risks unavailable due to API error")

    # Display main agent results if available
    if st.session_state.agent_results:
        results = st.session_state.agent_results

        st.divider()

        # Section 1: Agent Workflow Trace
        with st.expander("🧠 Agent Workflow Trace", expanded=False):
            for trace in results['react_trace']:
                phase = trace['phase']
                action = trace['action']
                observation = trace['observation']
                phase_emoji = {"REASON": "🤔", "ACT": "⚡", "OBSERVE": "👁️"}.get(phase, "•")
                st.markdown(f"""
                <span class="phase-badge">{phase}</span> {phase_emoji} {action}
                """, unsafe_allow_html=True)
                st.caption(f"👁️ {observation}")
                st.markdown("---")

        # Section 2: Knowledge Gap Forecast
        st.markdown("### 📡 Knowledge Gap Forecast")

        gap_forecast = results.get('gap_forecast', {})
        if hasattr(gap_forecast, 'at_risk_weeks') and gap_forecast.at_risk_weeks:
            # Sort by risk level (HIGH first)
            risk_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
            sorted_weeks = sorted(gap_forecast.at_risk_weeks, key=lambda w: risk_order.get(w.risk_level, 99))

            for week in sorted_weeks:
                severity_class = f"risk-{week.risk_level.lower()}"
                st.markdown(f"""
                <div class="at-risk-card">
                    <div>
                        <span class="risk-badge {severity_class}">{week.risk_level}</span>
                        <strong>Week {week.week}</strong> — {week.date}
                    </div>
                    <div><strong>Topic:</strong> {week.topic}</div>
                    <div><strong>Why:</strong> {week.reason}</div>
                    <div><strong>Prerequisite Gap:</strong> {week.prerequisite_gap}</div>
                    <div><strong>Recommended Prep:</strong> {week.recommended_prep}</div>
                    <div><strong>Hours Needed:</strong> {week.prep_hours_needed}h</div>
                </div>
                """, unsafe_allow_html=True)

            st.info(f"**Highest Risk:** {gap_forecast.highest_risk_week}")
            st.caption(f"**Summary:** {gap_forecast.summary}")
        else:
            st.info("No at-risk weeks identified or data unavailable.")

        # Section 3: Tonight's Study Plan
        st.markdown("### 📅 Tonight's Study Plan")

        tonight_plan = results.get('tonight_plan', {})
        if hasattr(tonight_plan, 'tonight_plan') and tonight_plan.tonight_plan:
            for slot in tonight_plan.tonight_plan:
                st.markdown(f"""
                <div class="timeline-block">
                    <div style="font-size: 1.1rem; font-weight: bold; color: #10b981;">
                        📌 {slot.slot}
                    </div>
                    <div><strong>Focus:</strong> {slot.assignment_or_topic}</div>
                    <div><strong>Action:</strong> {slot.action}</div>
                    <div><strong>Duration:</strong> {slot.duration_hours}h</div>
                    <div style="margin-top: 0.5rem; color: #9ca3af;">
                        💡 {slot.leverage_reason}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.info(f"**Expected Impact:** {tonight_plan.expected_impact}")

            if hasattr(tonight_plan, 'skipped') and tonight_plan.skipped:
                st.markdown("**Skipped (Lower Priority):**")
                for item in tonight_plan.skipped:
                    st.caption(f"• {item.name} — {item.reason}")
        else:
            st.info("No study plan available or data unavailable.")

        # Section 4: Cascade Risks
        st.markdown("### ⚡ Cascade Risks")

        cascade_risks = results.get('cascade_risks', {})
        if hasattr(cascade_risks, 'cascade_risks') and cascade_risks.cascade_risks:
            for risk in cascade_risks.cascade_risks:
                severity_class = f"risk-{risk.severity.lower()}"
                st.markdown(f"""
                <div class="cascade-card">
                    <div>
                        <span class="risk-badge {severity_class}">{risk.severity}</span>
                        <strong>{risk.trigger}</strong>
                    </div>
                    <div style="margin-top: 0.5rem;">
                        <strong>Consequence:</strong> {risk.consequence}
                    </div>
                    <div>
                        <strong>Affected:</strong> {', '.join(risk.affected_assignments)}
                    </div>
                    <div>
                        <strong>Impact in:</strong> {risk.time_to_impact}
                    </div>
                    <div style="margin-top: 0.5rem; color: #10b981;">
                        <strong>Action Now:</strong> {risk.action_now}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.info(f"""
            **Critical Path:** {cascade_risks.critical_path}

            *Canvas shows your grade. It cannot see this.*
            """)
        else:
            st.info("No cascade risks identified or data unavailable.")

        # Section 5: Autonomous Action Confirmed
        st.markdown("### ✅ Autonomous Action Confirmed")

        study_block = results.get('study_block_confirmed')
        if study_block:
            assignment = study_block.get('assignment', 'Unknown')
            start_time = study_block.get('scheduled_start', 'Unknown')
            duration = study_block.get('duration_hours', 0)
            st.success(f"""
            📅 <strong>{assignment}</strong> blocked for {start_time} · ⏰ {duration}h · ✅ Session confirmed
            """)

            overall_risk = results.get('overall_risk', 'UNKNOWN')
            risk_class = f"risk-{overall_risk.lower()}"
            st.markdown(f"""
            <div style="margin-top: 1rem;">
                <span class="risk-badge {risk_class}">Overall Risk: {overall_risk}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No study session was confirmed.")


if __name__ == "__main__":
    main()
