import React, { useEffect, useState } from 'react';
import { 
  BarChart3, 
  CheckCircle2, 
  Flame, 
  Clock, 
  AlertTriangle, 
  Sparkles, 
  Loader2, 
  Layers,
  Target,
  ArrowRight
} from 'lucide-react';
import { dsaApi } from '../services/api';
import { StatsCard } from '../components/StatsCard';
import { ProgressBar } from '../components/ProgressBar';
import { WeakTopicAlert } from '../components/WeakTopicAlert';

export const ProgressDashboard = () => {
  const [progressData, setProgressData] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    Promise.all([
      dsaApi.getProgress(),
      dsaApi.getRecommendations()
    ])
      .then(([prog, recs]) => {
        setProgressData(prog);
        setRecommendations(recs);
      })
      .catch((err) => console.error(err))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center flex flex-col items-center gap-4">
        <Loader2 className="w-10 h-10 animate-spin text-brand-400" />
        <span className="text-base font-semibold text-slate-300">Calculating your performance metrics...</span>
      </div>
    );
  }

  const {
    total_problems = 0,
    completed = 0,
    in_progress = 0,
    not_started = 0,
    skipped = 0,
    completion_percentage = 0,
    current_streak = 1,
    estimated_hours_left = 0,
    topic_breakdown = [],
    difficulty_breakdown = {},
    weak_topics = []
  } = progressData || {};

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col gap-8">
      {/* Header Banner */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/30">
            Analytics & Mastery
          </span>
        </div>
        <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
          DSA Preparation Progress
        </h1>
        <p className="text-sm sm:text-base text-slate-300">
          Track problem completion, concept retention, and AI-detected weak topic recommendations.
        </p>
      </div>

      {/* Top Metrics Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <StatsCard
          title="Completion Rate"
          value={`${completion_percentage}%`}
          subtitle={`${completed} of ${total_problems} solved`}
          color="emerald"
          icon={CheckCircle2}
        />
        <StatsCard
          title="Current Streak"
          value={`${current_streak} Days`}
          subtitle="Consistency multiplier"
          color="amber"
          icon={Flame}
        />
        <StatsCard
          title="In Progress"
          value={in_progress}
          subtitle={`${not_started} not started yet`}
          color="brand"
          icon={Layers}
        />
        <StatsCard
          title="Est. Time Left"
          value={`${estimated_hours_left}h`}
          subtitle="At ~35 min per problem"
          color="purple"
          icon={Clock}
        />
      </div>

      {/* Overall Progress Bar Card (Section 15 format) */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col gap-4 shadow-sm">
        <h3 className="text-base font-bold text-white flex items-center justify-between">
          <span>Overall Roadmap Progress</span>
          <span className="text-sm text-brand-400 font-extrabold">{completion_percentage}%</span>
        </h3>
        
        <ProgressBar
          percentage={completion_percentage}
          completed={completed}
          total={total_problems}
          label=""
          showDetails={false}
          color="brand"
        />

        <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800/80">
          <span>Completed: <strong className="text-emerald-400">{completed}</strong></span>
          <span>In Progress: <strong className="text-blue-400">{in_progress}</strong></span>
          <span>Skipped: <strong className="text-slate-400">{skipped}</strong></span>
          <span>Remaining: <strong className="text-amber-400">{total_problems - completed}</strong></span>
        </div>
      </div>

      {/* Weak Topic Alert & Recommendations (Section 16 requirement) */}
      {weak_topics && weak_topics.length > 0 && (
        <WeakTopicAlert
          weakTopics={weak_topics}
          recommendations={recommendations?.recommendations || []}
        />
      )}

      {/* Topic Mastery Breakdown */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 flex flex-col gap-6 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white">
              Topic Mastery & Retention
            </h2>
            <p className="text-xs text-slate-400">
              Track your proficiency across core DSA algorithms.
            </p>
          </div>
          <span className="text-xs text-slate-400 hidden sm:block">
            Threshold for mastery: 50%+
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5">
          {topic_breakdown.map((item) => (
            <div key={item.topic} className="flex flex-col gap-1.5">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-slate-200">{item.topic}</span>
                  {item.is_weak && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                      Weak Topic
                    </span>
                  )}
                </div>
                <span className="text-slate-400 font-medium">
                  {item.completed} / {item.total} ({item.percentage}%)
                </span>
              </div>

              <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    item.is_weak
                      ? 'bg-amber-500'
                      : item.percentage >= 80
                      ? 'bg-emerald-500'
                      : 'bg-brand-500'
                  }`}
                  style={{ width: `${Math.min(100, item.percentage)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Difficulty Breakdown */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {['Easy', 'Medium', 'Hard'].map((diff) => {
          const stat = difficulty_breakdown[diff] || { total: 0, completed: 0 };
          const pct = stat.total > 0 ? Math.round((stat.completed / stat.total) * 100) : 0;
          return (
            <div key={diff} className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-white">{diff} Problems</span>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                  {pct}% Solved
                </span>
              </div>
              <span className="text-xl font-extrabold text-white">
                {stat.completed} / {stat.total}
              </span>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden mt-1">
                <div
                  className={`h-full rounded-full ${
                    diff === 'Easy' ? 'bg-emerald-500' : diff === 'Medium' ? 'bg-amber-500' : 'bg-rose-500'
                  }`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
