import { useAgentRun } from './hooks/useAgentRun';
import { Nav } from './components/Nav';
import { HeroSection } from './components/HeroSection';
import { AgentStepper } from './components/AgentStepper';
import { GapForecastCard } from './components/GapForecastCard';
import { StudyPlanCard } from './components/StudyPlanCard';
import { CascadeRisksCard } from './components/CascadeRisksCard';
import { ActionCard } from './components/ActionCard';

function App() {
  const {
    state,
    results,
    whatIfResults,
    error,
    currentStep,
    runAgent,
    runWhatIf,
  } = useAgentRun();

  const isLoading = state === 'running';
  const hasResults = state === 'complete';

  // Determine which cascade risks to show (what-if or original)
  const cascadeRisksToShow = whatIfResults?.cascade_risks || results?.cascade_risks;
  const isWhatIfMode = whatIfResults !== null;

  return (
    <div className="min-h-screen bg-base bg-grid-pattern bg-grid text-text-primary">
      <Nav />

      <main className="max-w-7xl mx-auto px-6 pb-12">
        <HeroSection
          onRunAgent={runAgent}
          onWhatIf={() => runWhatIf('Workbook 2')}
          results={results}
          isRunning={isLoading}
        />

        {/* Error state */}
        {error && (
          <div className="card mb-6 border-l-4 border-accent-red">
            <h3 className="text-xl font-display font-semibold text-accent-red mb-2">
              Error
            </h3>
            <p className="text-text-muted">{error}</p>
            <button
              onClick={runAgent}
              className="mt-4 btn btn-primary"
            >
              Retry
            </button>
          </div>
        )}

        {/* Agent stepper */}
        {isLoading && (
          <AgentStepper
            currentStep={currentStep}
            reactTrace={results?.react_trace || []}
          />
        )}

        {/* Results grid */}
        {(isLoading || hasResults) && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Knowledge Gap Forecast - Full width */}
            <div className="lg:col-span-2">
              <GapForecastCard
                weeks={results?.gap_forecast?.at_risk_weeks || []}
                isLoading={isLoading}
              />
            </div>

            {/* Tonight's Study Plan - Left column */}
            <div className="lg:col-span-1">
              <StudyPlanCard
                plan={results?.tonight_plan || null}
                isLoading={isLoading}
              />
            </div>

            {/* Cascade Risks - Right column */}
            <div className="lg:col-span-1">
              <CascadeRisksCard
                risks={cascadeRisksToShow || null}
                isLoading={isLoading}
                isWhatIf={isWhatIfMode}
              />
            </div>

            {/* Autonomous Action - Full width */}
            <div className="lg:col-span-2">
              <ActionCard
                studyBlock={results?.study_block_confirmed || null}
                overallRisk={results?.overall_risk || null}
                isLoading={isLoading}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
