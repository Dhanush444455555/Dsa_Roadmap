import React from 'react';

export const ProgressBar = ({ 
  percentage = 0, 
  completed = 0, 
  total = 0, 
  label = 'DSA Progress', 
  color = 'brand',
  showDetails = true 
}) => {
  const safePct = Math.min(100, Math.max(0, percentage));

  const getColorGradient = () => {
    switch (color) {
      case 'emerald':
        return 'from-emerald-500 to-teal-400';
      case 'amber':
        return 'from-amber-500 to-orange-400';
      case 'purple':
        return 'from-purple-500 to-indigo-500';
      case 'brand':
      default:
        return 'from-brand-500 via-indigo-500 to-purple-500';
    }
  };

  return (
    <div className="w-full flex flex-col gap-1.5">
      {showDetails && (
        <div className="flex items-center justify-between text-xs sm:text-sm">
          <span className="font-semibold text-slate-200">{label}</span>
          <div className="flex items-center gap-2">
            <span className="font-bold text-white">{safePct}%</span>
            {total > 0 && (
              <span className="text-slate-400 text-xs">
                ({completed} / {total} completed)
              </span>
            )}
          </div>
        </div>
      )}

      {/* Progress Track */}
      <div className="h-2.5 w-full bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700/50">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${getColorGradient()} transition-all duration-500 ease-out shadow-sm`}
          style={{ width: `${safePct}%` }}
        />
      </div>
    </div>
  );
};
