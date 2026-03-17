import { motion } from 'framer-motion';

interface StatPillProps {
  label: string;
  value: string | number;
  accent?: 'red' | 'amber' | 'green' | 'blue' | 'cyan';
}

export const StatPill = ({ label, value, accent = 'blue' }: StatPillProps) => {
  const accentColors = {
    red: 'text-accent-red',
    amber: 'text-accent-amber',
    green: 'text-accent-green',
    blue: 'text-accent-blue',
    cyan: 'text-accent-cyan',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex items-center gap-2 px-4 py-2 bg-surface border border-border rounded-lg"
    >
      <span className="text-text-muted text-sm">{label}</span>
      <span className={`font-mono font-bold ${accentColors[accent]}`}>
        {value}
      </span>
    </motion.div>
  );
};
