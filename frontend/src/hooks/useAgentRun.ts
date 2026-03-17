import { useState, useCallback } from 'react';
import { AgentResults, WhatIfResults, UIState } from '../types/agent';

const API_BASE_URL = '/api';

export const useAgentRun = () => {
  const [state, setState] = useState<UIState>('idle');
  const [results, setResults] = useState<AgentResults | null>(null);
  const [whatIfResults, setWhatIfResults] = useState<WhatIfResults | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState(0);

  const runAgent = useCallback(async () => {
    setState('running');
    setError(null);
    setCurrentStep(0);
    setResults(null);
    setWhatIfResults(null);

    try {
      const response = await fetch(`${API_BASE_URL}/run-agent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: AgentResults = await response.json();
      setResults(data);
      setState('complete');
      setCurrentStep(5); // All steps complete

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      setState('error');
    }
  }, []);

  const runWhatIf = useCallback(async (skipAssignment: string) => {
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/whatif`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ skip_assignment: skipAssignment }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: WhatIfResults = await response.json();
      setWhatIfResults(data);

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
    }
  }, []);

  return {
    state,
    results,
    whatIfResults,
    error,
    currentStep,
    runAgent,
    runWhatIf,
  };
};
