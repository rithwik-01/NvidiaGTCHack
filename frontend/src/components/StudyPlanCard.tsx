import { motion } from 'framer-motion';
import { TonightPlan } from '../types/agent';
import { StudyPlanTimeline } from './StudyPlanTimeline';

interface StudyPlanCardProps {
  plan: TonightPlan | null;
  isLoading: boolean;
}

export const StudyPlanCard = ({ plan, isLoading }: StudyPlanCardProps) => {
  if (isLoading) {
    return <div className="card mb-6"><div className="animate-pulse h-6 bg-elevated rounded w-1/3 mb-4"></div><div className="space-y-3"><div className="h-4 bg-elevated rounded"></div><div className="h-4 bg-elevated rounded w-5/6"></div></div></div>;
  }

  if (!plan || !plan.tonight_plan || plan.tonight_plan.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card card-hover-glow-blue mb-6"
      >
        <h3 className="text-xl font-display font-semibold text-white mb-4 flex items-center gap-2">
          <span>📅</span>
          Tonight's Study Plan
        </h3>
        <p className="text-text-muted">No study plan available.</p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card card-hover-glow-blue mb-6"
    >
      <h3 className="text-xl font-display font-semibold text-white mb-4 flex items-center gap-2">
        <span>📅</span>
        Tonight's Study Plan
      </h3>

      <StudyPlanTimeline
        slots={plan.tonight_plan}
        expectedImpact={plan.expected_impact}
      />

      {plan.skipped && plan.skipped.length > 0 && (
        <div className="mt-6 pt-4 border-t border-border">
          <div className="text-text-muted text-sm font-medium mb-2">
            Skipped (deprioritized):
          </div>
          <div className="space-y-2">
            {plan.skipped.map((item, index) => (
              <div key={index} className="text-sm text-text-muted">
                <span className="text-white">{item.name}</span>
                <span className="ml-2 text-xs">
                  — {item.reason}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
};
