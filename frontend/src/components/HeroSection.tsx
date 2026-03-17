import { motion } from 'framer-motion';
import { AgentResults } from '../types/agent';

interface HeroSectionProps {
  onRunAgent: () => void;
  onWhatIf: () => void;
  results: AgentResults | null;
  isRunning: boolean;
}

export const HeroSection = ({ onRunAgent, onWhatIf, results, isRunning }: HeroSectionProps) => {
  const nGaps = results?.gap_forecast?.at_risk_weeks?.length || 0;
  const nRisks = results?.cascade_risks?.cascade_risks?.length || 0;
  const overallRisk = results?.overall_risk || null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="text-center mb-12 pt-20"
    >
      <h1 className="text-5xl md:text-6xl font-display font-bold text-white mb-4">
        See what Canvas cannot.
      </h1>
      <p className="text-xl text-text-muted mb-8 max-w-2xl mx-auto">
        3 specialized AI agents reasoning over your academic trajectory
      </p>

      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onRunAgent}
          disabled={isRunning}
          className={`btn btn-primary text-lg px-8 py-4 ${isRunning ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isRunning ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Agent thinking...
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <span>▶</span>
              Run Agent
            </span>
          )}
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onWhatIf}
          disabled={!results}
          className={`btn btn-secondary ${!results ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <span className="flex items-center gap-2">
            <span>🔀</span>
            What-if: Skip Workbook 2?
          </span>
        </motion.button>
      </div>

      {/* Stats pills */}
      {results && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="flex flex-wrap items-center justify-center gap-3"
        >
          <span className="text-text-muted">
            {nGaps} gaps found
          </span>
          <span className="text-text-muted">·</span>
          <span className="text-text-muted">
            {nRisks} cascade risks
          </span>
          <span className="text-text-muted">·</span>
          {overallRisk && (
            <span className={`font-mono font-bold ${
              overallRisk === 'HIGH' ? 'text-accent-red' :
              overallRisk === 'MEDIUM' ? 'text-accent-amber' :
              'text-accent-green'
            }`}>
              Overall: {overallRisk}
            </span>
          )}
        </motion.div>
      )}
    </motion.div>
  );
};
