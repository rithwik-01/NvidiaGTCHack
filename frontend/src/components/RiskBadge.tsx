import { RiskLevel } from '../types/agent';

interface RiskBadgeProps {
  level: RiskLevel;
  className?: string;
}

export const RiskBadge = ({ level, className = '' }: RiskBadgeProps) => {
  return (
    <span className={`risk-badge risk-badge-${level} ${className}`}>
      {level}
    </span>
  );
};
