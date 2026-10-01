import React from 'react';
import { AlertTriangle, Sparkles, ArrowRight, ExternalLink } from 'lucide-react';
import { dsaApi } from '../services/api';

export const WeakTopicAlert = ({ weakTopics = [], recommendations = [] }) => {
  if (!weakTopics || weakTopics.length === 0) return null;

  return (
    <div className="bg-gradient-to-r from-amber-950/40 via-slate-900/90 to-purple-950/40 border border-amber-500/30 rounded-2xl p-5 sm:p-6 flex flex-col gap-4 shadow-lg">
      <div className="flex items-start gap-3">
        <div className="p-2.5 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/30 shrink-0">
          <AlertTriangle className="w-5 h-5" />
        </div>
        <div className="flex flex-col gap-1">
          <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            Weak Topic Reinforcement Detected
            <span className="text-xs font-semibold px-2 py-0.5 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded-full">
              AI Insight
            </span>
          </h3>
          <p className="text-sm text-slate-300">
            Your performance in <strong className="text-amber-300">{weakTopics.join(', ')}</strong> is currently lower than other areas. We've selected targeted problems to build your intuition.
          </p>
        </div>
      </div>

      {/* Recommendations Cards */}
      {recommendations && recommendations.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 pt-2">
          {recommendations.map((rec, idx) => {
            const leetcodeUrl = dsaApi.getLeetCodeUrl(rec.leetcode_number, rec.slug, rec.title);
            return (
              <div 
                key={idx}
                className="bg-slate-950/80 border border-slate-800 hover:border-amber-500/40 rounded-xl p-3.5 flex flex-col justify-between gap-2 transition-all"
              >
                <div className="flex flex-col gap-1">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                      {rec.topic}
                    </span>
                    <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
                      rec.difficulty === 'Easy' ? 'text-emerald-400 bg-emerald-500/10' :
                      rec.difficulty === 'Hard' ? 'text-rose-400 bg-rose-500/10' :
                      'text-amber-400 bg-amber-500/10'
                    }`}>
                      {rec.difficulty}
                    </span>
                  </div>
                  <span className="text-sm font-semibold text-white line-clamp-1">
                    {rec.leetcode_number ? `${rec.leetcode_number} — ` : ''}{rec.title}
                  </span>
                  <p className="text-[11px] text-slate-400 line-clamp-2">
                    {rec.reason}
                  </p>
                </div>

                <a
                  href={leetcodeUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-1 flex items-center justify-between text-xs font-medium text-brand-400 hover:text-brand-300 bg-brand-500/10 hover:bg-brand-500/20 px-2.5 py-1.5 rounded-lg transition-colors"
                >
                  <span>Practice Problem</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
