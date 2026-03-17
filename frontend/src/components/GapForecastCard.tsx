import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { RiskBadge } from './RiskBadge';
import { AtRiskWeek } from '../types/agent';

interface GapForecastCardProps {
  weeks: AtRiskWeek[];
  isLoading: boolean;
}

export const GapForecastCard = ({ weeks, isLoading }: GapForecastCardProps) => {
  if (isLoading) {
    return <div className="card mb-6"><div className="animate-pulse h-6 bg-elevated rounded w-1/3 mb-4"></div><div className="space-y-3"><div className="h-4 bg-elevated rounded"></div><div className="h-4 bg-elevated rounded w-5/6"></div></div></div>;
  }

  if (!weeks || weeks.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card card-hover-glow-green mb-6"
      >
        <h3 className="text-xl font-display font-semibold text-white mb-4 flex items-center gap-2">
          <span>🧠</span>
          Knowledge Gap Forecast
        </h3>
        <p className="text-text-muted">No knowledge gaps detected. You're on track!</p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card card-hover-glow-red mb-6"
    >
      <h3 className="text-xl font-display font-semibold text-white mb-4 flex items-center gap-2">
        <span>🧠</span>
        Knowledge Gap Forecast
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {weeks.map((week, index) => (
          <motion.div
            key={week.week}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="bg-elevated border border-border rounded-lg p-4 hover:-translate-y-1 transition-transform"
          >
            <div className="flex items-start justify-between mb-2">
              <div>
                <div className="font-mono text-accent-cyan text-sm">
                  Week {week.week}
                </div>
                <div className="font-mono text-text-muted text-xs">
                  {format(new Date(week.date), 'MMM d')}
                </div>
              </div>
              <RiskBadge level={week.risk_level} />
            </div>

            <div className="mb-2">
              <div className="text-white font-medium mb-1">{week.topic}</div>
              <div className="text-text-muted text-sm">
                Gap: {week.prerequisite_gap}
              </div>
            </div>

            <div className="text-accent-cyan text-sm italic mb-2">
              {week.recommended_prep}
            </div>

            <div className="font-mono text-xs text-text-muted">
              {week.prep_hours_needed}h prep needed
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};
