import { motion } from 'framer-motion';
import { CascadeRisk } from '../types/agent';

interface CascadeRisksStackProps {
  risks: CascadeRisk[];
  title?: string;
}

export const CascadeRisksStack = ({ risks }: CascadeRisksStackProps) => {
  if (!risks || risks.length === 0) {
    return (
      <div className="text-text-muted">
        No cascade risks detected. You're in good shape!
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {risks.map((risk, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: index * 0.1 }}
          className={`border border-border rounded-lg p-4 hover:-translate-y-1 transition-transform ${
            risk.severity === 'HIGH' ? 'hover:shadow-lg hover:shadow-accent-red/20 hover:border-accent-red/50' :
            risk.severity === 'MEDIUM' ? 'hover:shadow-lg hover:shadow-accent-amber/20 hover:border-accent-amber/50' :
            'hover:shadow-lg hover:shadow-accent-green/20 hover:border-accent-green/50'
          }`}
        >
          {/* Header */}
          <div className="flex items-start justify-between mb-3">
            <span className={`text-xs font-bold uppercase tracking-wide ${
              risk.severity === 'HIGH' ? 'text-accent-red' :
              risk.severity === 'MEDIUM' ? 'text-accent-amber' :
              'text-accent-green'
            }`}>
              {risk.severity} SEVERITY
            </span>
            <span className="text-xs font-mono text-accent-cyan bg-elevated px-2 py-1 rounded">
              {risk.time_to_impact}
            </span>
          </div>

          {/* Flow */}
          <div className="flex items-center gap-2 mb-3">
            <div className="flex-1">
              <div className="text-white text-sm">{risk.trigger}</div>
            </div>
            <span className="text-text-muted">→</span>
            <div className="flex-1">
              <div className="text-white text-sm">{risk.consequence}</div>
            </div>
          </div>

          {/* Affected assignments */}
          {risk.affected_assignments && risk.affected_assignments.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-3">
              {risk.affected_assignments.map((assignment, idx) => (
                <span
                  key={idx}
                  className="text-xs bg-elevated text-text-muted px-2 py-1 rounded"
                >
                  {assignment}
                </span>
              ))}
            </div>
          )}

          {/* Action */}
          <div className="text-accent-green text-sm">
            {risk.action_now}
          </div>
        </motion.div>
      ))}

      {/* Footer callout */}
      <div className="text-center text-text-muted italic text-sm pt-4">
        Canvas shows your grade. It cannot see this.
      </div>
    </div>
  );
};
