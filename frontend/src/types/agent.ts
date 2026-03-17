// Agent Types
export type RiskLevel = 'HIGH' | 'MEDIUM' | 'LOW';
export type Phase = 'REASON' | 'ACT' | 'OBSERVE';

export interface ReactTrace {
  phase: Phase;
  action: string;
  observation: string;
  timestamp: string;
}

export interface AtRiskWeek {
  week: number;
  date: string;
  topic: string;
  risk_level: RiskLevel;
  reason: string;
  prerequisite_gap: string;
  recommended_prep: string;
  prep_hours_needed: number;
}

export interface GapForecast {
  at_risk_weeks: AtRiskWeek[];
  highest_risk_week: string;
  summary: string;
}

export interface TonightSlot {
  slot: string;
  assignment_or_topic: string;
  action: string;
  duration_hours: number;
  leverage_reason: string;
}

export interface SkippedItem {
  name: string;
  reason: string;
}

export interface TonightPlan {
  tonight_plan: TonightSlot[];
  skipped: SkippedItem[];
  expected_impact: string;
}

export interface CascadeRisk {
  trigger: string;
  consequence: string;
  affected_assignments: string[];
  severity: RiskLevel;
  time_to_impact: string;
  action_now: string;
}

export interface CascadeRisks {
  cascade_risks: CascadeRisk[];
  critical_path: string;
  invisible_to_canvas: string;
}

export interface StudyBlockConfirmed {
  assignment: string;
  scheduled_start: string;
  duration_hours: number;
  status: string;
  message: string;
}

export interface AgentResults {
  gap_forecast: GapForecast;
  tonight_plan: TonightPlan;
  cascade_risks: CascadeRisks;
  study_block_confirmed: StudyBlockConfirmed | null;
  react_trace: ReactTrace[];
  overall_risk: RiskLevel;
}

export interface WhatIfResults {
  cascade_risks: CascadeRisks;
  skipped_assignment: string;
  scenario: string;
}

// API Types
export interface RunAgentRequest {}

export interface WhatIfRequest {
  skip_assignment: string;
}

// UI State Types
export interface AgentStep {
  id: number;
  label: string;
  icon: string;
  status: 'pending' | 'active' | 'completed';
}

export type UIState = 'idle' | 'running' | 'complete' | 'error';
