import { motion } from 'framer-motion';
import { ReactTrace, AgentStep } from '../types/agent';

interface AgentStepperProps {
  currentStep: number;
  reactTrace: ReactTrace[];
}

const steps: AgentStep[] = [
  { id: 1, label: 'Load Data', icon: '📚', status: 'pending' },
  { id: 2, label: 'Gap Forecast', icon: '📡', status: 'pending' },
  { id: 3, label: 'Study Plan', icon: '📅', status: 'pending' },
  { id: 4, label: 'Cascade Risks', icon: '⚡', status: 'pending' },
  { id: 5, label: 'Action', icon: '✅', status: 'pending' },
];

export const AgentStepper = ({ currentStep, reactTrace }: AgentStepperProps) => {
  const getStepStatus = (stepId: number) => {
    if (stepId < currentStep) return 'completed';
    if (stepId === currentStep) return 'active';
    return 'pending';
  };

  const getCurrentAction = () => {
    if (currentStep === 0) return null;
    const trace = reactTrace[currentStep - 1];
    return trace?.observation || '';
  };

  const currentAction = getCurrentAction();

  return (
    <div className="mb-12">
      <div className="flex items-center justify-center gap-4 mb-6">
        {steps.map((step, index) => {
          const status = getStepStatus(step.id);
          const isActive = status === 'active';
          const isCompleted = status === 'completed';

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="flex flex-col items-center gap-2"
            >
              <div
                className={`
                  w-12 h-12 rounded-full flex items-center justify-center text-xl
                  transition-all duration-300
                  ${isActive ? 'bg-accent-blue text-white shadow-lg shadow-accent-blue/50 scale-110' : ''}
                  ${isCompleted ? 'bg-accent-green text-white' : ''}
                  ${status === 'pending' ? 'bg-surface text-text-muted border border-border' : ''}
                `}
              >
                {isCompleted ? '✓' : step.icon}
              </div>
              <span
                className={`text-xs font-medium uppercase tracking-wide ${
                  isActive ? 'text-accent-blue' : isCompleted ? 'text-accent-green' : 'text-text-muted'
                }`}
              >
                {step.label}
              </span>
            </motion.div>
          );
        })}
      </div>

      {/* Current action */}
      {currentAction && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <span className="text-text-muted italic">{currentAction}</span>
        </motion.div>
      )}
    </div>
  );
};
