import { motion } from 'framer-motion';
import { TonightSlot } from '../types/agent';

interface StudyPlanTimelineProps {
  slots: TonightSlot[];
  expectedImpact: string;
}

export const StudyPlanTimeline = ({ slots, expectedImpact }: StudyPlanTimelineProps) => {
  return (
    <div>
      {/* Timeline */}
      <div className="relative pl-8">
        {/* Vertical line */}
        <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-border"></div>

        {slots.map((slot, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="relative mb-6 last:mb-0"
          >
            {/* Dot */}
            <div className="absolute left-[-8px] top-1 w-4 h-4 bg-accent-cyan rounded-full border-2 border-base"></div>

            {/* Time */}
            <div className="font-mono text-accent-cyan text-sm mb-1">
              {slot.slot}
            </div>

            {/* Assignment */}
            <div className="text-white font-medium mb-1">
              {slot.assignment_or_topic}
            </div>

            {/* Action */}
            <div className="text-text-muted text-sm mb-2">
              {slot.action}
            </div>

            {/* Leverage reason */}
            <div className="text-xs text-text-muted italic">
              Leverage: {slot.leverage_reason}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Expected impact callout */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: slots.length * 0.1 }}
        className="mt-6 p-4 bg-elevated border-l-4 border-accent-green rounded-r-lg"
      >
        <div className="text-accent-green font-medium text-sm mb-1">
          Expected Impact
        </div>
        <div className="text-text-muted text-sm">
          {expectedImpact}
        </div>
      </motion.div>
    </div>
  );
};
