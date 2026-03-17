import { motion } from 'framer-motion';
import { CascadeRisks } from '../types/agent';
import { CascadeRisksStack } from './CascadeRisksStack';

interface CascadeRisksCardProps {
  risks: CascadeRisks | null;
  isLoading: boolean;
  isWhatIf?: boolean;
}

export const CascadeRisksCard = ({ risks, isLoading, isWhatIf = false }: CascadeRisksCardProps) => {
  if (isLoading) {
    return <div className="card mb-6"><div className="animate-pulse h-6 bg-elevated rounded w-1/3 mb-4"></div><div className="space-y-3"><div className="h-4 bg-elevated rounded"></div><div className="h-4 bg-elevated rounded w-5/6"></div></div></div>;
  }

  if (!risks) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card card-hover-glow-amber mb-6"
      >
        <h3 className="text-xl font-display font-semibold text-white mb-4 flex items-center gap-2">
          <span>⚡</span>
          Cascade Risks
        </h3>
        <p className="text-text-muted">No cascade risks detected.</p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card card-hover-glow-amber mb-6"
    >
      <h3 className="text-xl font-display font-semibold text-white mb-4 flex items-center gap-2">
        <span>⚡</span>
        {isWhatIf ? "What-if: No Workbook 2?" : "Cascade Risks"}
      </h3>

      <CascadeRisksStack
        risks={risks.cascade_risks}
        title={isWhatIf ? "What-if Analysis" : undefined}
      />

      {risks.critical_path && (
        <div className="mt-6 pt-4 border-t border-border">
          <div className="text-text-muted text-sm font-medium mb-1">
            Critical Path:
          </div>
          <div className="text-white text-sm">
            {risks.critical_path}
          </div>
        </div>
      )}

      {risks.invisible_to_canvas && (
        <div className="mt-4 text-text-muted italic text-sm">
          {risks.invisible_to_canvas}
        </div>
      )}
    </motion.div>
  );
};
