export const SkeletonCard = () => {
  return (
    <div className="card animate-pulse">
      <div className="h-6 bg-elevated rounded w-1/3 mb-4"></div>
      <div className="space-y-3">
        <div className="h-4 bg-elevated rounded"></div>
        <div className="h-4 bg-elevated rounded w-5/6"></div>
        <div className="h-4 bg-elevated rounded w-4/6"></div>
      </div>
    </div>
  );
};
