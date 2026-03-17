import { motion } from 'framer-motion';
import { StudyBlockConfirmed, RiskLevel } from '../types/agent';
import { DonutChart } from './DonutChart';

interface ActionCardProps {
  studyBlock: StudyBlockConfirmed | null;
  overallRisk: RiskLevel | null;
  isLoading: boolean;
}

export const ActionCard = ({ studyBlock, overallRisk, isLoading }: ActionCardProps) => {
  if (isLoading) {
    return <div className="card mb-6"><div className="animate-pulse h-6 bg-elevated rounded w-1/3 mb-4"></div><div className="space-y-3"><div className="h-4 bg-elevated rounded"></div><div className="h-4 bg-elevated rounded w-5/6"></div></div></div>;
  }

  if (!studyBlock) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card card-hover-glow-green mb-6"
      >
        <h3 className="text-xl font-display font-semibold text-white mb-4 flex items-center gap-2">
          <span>✅</span>
          Autonomous Action Confirmed
        </h3>
        <p className="text-text-muted">No study block confirmed.</p>
      </motion.div>
    );
  }

  // Mock grade category data for donut chart
  const gradeData = [
    { name: 'Participation', value: 85, color: '#10B981' },
    { name: 'Quizzes', value: 40, color: '#F59E0B' },
    { name: 'Midterm', value: 0, color: '#3B82F6' },
    { name: 'Final', value: 0, color: '#06B6D4' },
  ].filter(item => item.value > 0);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`card card-hover-glow-green mb-6 border-l-4 ${
        overallRisk === 'HIGH' ? 'border-l-accent-red' :
        overallRisk === 'MEDIUM' ? 'border-l-accent-amber' :
        'border-l-accent-green'
      }`}
    >
      <h3 className="text-xl font-display font-semibold text-white mb-4 flex items-center gap-2">
        <span>✅</span>
        Autonomous Action Confirmed
      </h3>

      <div className="flex flex-col md:flex-row items-start justify-between gap-6">
        {/* Left: Study block confirmation */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-4xl">📅</span>
            <div>
              <div className="text-white font-medium">
                {studyBlock.assignment}
              </div>
              <div className="text-text-muted text-sm">
                {studyBlock.scheduled_start} · ⏰ {studyBlock.duration_hours}h · ✅
              </div>
            </div>
          </div>

          <div className="text-accent-green text-sm mb-4">
            {studyBlock.message}
          </div>

          {/* Overall risk badge */}
          {overallRisk && (
            <div className="flex justify-center">
              <span className={`px-6 py-3 rounded-lg text-2xl font-bold uppercase tracking-wide ${
                overallRisk === 'HIGH' ? 'bg-accent-red/20 text-accent-red animate-pulse-slow' :
                overallRisk === 'MEDIUM' ? 'bg-accent-amber/20 text-accent-amber' :
                'bg-accent-green/20 text-accent-green'
              }`}>
                Overall Risk: {overallRisk}
              </span>
            </div>
          )}
        </div>

        {/* Right: Donut chart */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex-shrink-0"
        >
          <DonutChart data={gradeData} />
        </motion.div>
      </div>
    </motion.div>
  );
};
