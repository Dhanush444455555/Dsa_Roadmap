import React from 'react';

export const StatsCard = ({ title, value, subtitle, icon: Icon, color = 'brand' }) => {
  const getIconContainerStyles = () => {
    switch (color) {
      case 'emerald':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
      case 'amber':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
      case 'purple':
        return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
      case 'rose':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
      case 'brand':
      default:
        return 'bg-brand-500/10 text-brand-400 border-brand-500/20';
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 sm:p-5 flex items-center justify-between shadow-sm">
      <div className="flex flex-col gap-1">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          {title}
        </span>
        <span className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          {value}
        </span>
        {subtitle && (
          <span className="text-xs text-slate-400 font-medium">
            {subtitle}
          </span>
        )}
      </div>

      {Icon && (
        <div className={`p-3 rounded-xl border ${getIconContainerStyles()}`}>
          <Icon className="w-6 h-6" />
        </div>
      )}
    </div>
  );
};
