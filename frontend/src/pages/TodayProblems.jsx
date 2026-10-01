import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  CheckCircle2, 
  Calendar, 
  Sparkles, 
  Flame, 
  ArrowRight, 
  Loader2, 
  Trophy, 
  BookOpen,
  RotateCcw
} from 'lucide-react';
import { dsaApi } from '../services/api';
import { ProblemCard } from '../components/ProblemCard';
import { ProgressBar } from '../components/ProgressBar';

export const TodayProblems = () => {
  const [todayData, setTodayData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchToday = () => {
    setIsLoading(true);
    dsaApi.getTodayProblems()
      .then((res) => {
        setTodayData(res);
      })
      .catch((err) => console.error(err))
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    fetchToday();
  }, []);

  const handleStatusChange = (itemId, newStatus) => {
    if (!todayData) return;
    const updatedProbs = todayData.problems.map((p) => {
      if (p.id === itemId || p.roadmap_item_id === itemId) {
        return { ...p, status: newStatus };
      }
      return p;
    });

    const completedToday = updatedProbs.filter((p) => p.status === 'Completed').length;
    setTodayData({
      ...todayData,
      problems: updatedProbs,
      completed_today: completedToday
    });
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center flex flex-col items-center gap-4">
        <Loader2 className="w-10 h-10 animate-spin text-brand-400" />
        <span className="text-base font-semibold text-slate-300">Fetching today's practice schedule...</span>
      </div>
    );
  }

  const problems = todayData?.problems || [];
  const completedToday = todayData?.completed_today || 0;
  const totalToday = problems.length;
  const isAllCompleted = totalToday > 0 && completedToday === totalToday;
  const weekNum = todayData?.week || 1;
  const dayNum = todayData?.day || 1;
  const focusTopic = todayData?.focus_topic || 'General DSA';

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col gap-8">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-xl">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
              Week {weekNum} • Day {dayNum}
            </span>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              Topic: {focusTopic}
            </span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
            Today's Problems
          </h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Complete today's designated problems to build consistent mastery and maintain your learning streak.
          </p>
        </div>

        {/* Quick Actions */}
        <div className="flex items-center gap-2 shrink-0">
          <Link
            to="/roadmap"
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 transition-colors shadow-sm inline-flex items-center gap-1.5"
          >
            <Calendar className="w-3.5 h-3.5" />
            Full Roadmap
          </Link>
          <Link
            to="/revision"
            className="px-4 py-2.5 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-xs font-semibold text-purple-300 transition-colors shadow-sm inline-flex items-center gap-1.5"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Revision List
          </Link>
        </div>
      </div>

      {/* Progress Bar for Today */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 sm:p-5">
        <ProgressBar
          percentage={totalToday > 0 ? Math.round((completedToday / totalToday) * 100) : 100}
          completed={completedToday}
          total={totalToday}
          label="Today's Target Completion"
          color="emerald"
        />
      </div>

      {/* All Done Celebration Alert */}
      {isAllCompleted && (
        <div className="bg-emerald-950/40 border border-emerald-500/40 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-lg">
          <div className="flex items-center gap-4">
            <div className="p-3 rounded-2xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
              <Trophy className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">
                Outstanding! All Daily Targets Completed
              </h3>
              <p className="text-xs text-slate-300">
                You've solved all designated problems for today. Your spaced revision schedules have been queued.
              </p>
            </div>
          </div>

          <Link
            to="/roadmap"
            className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-5 py-2.5 rounded-xl shadow-md transition-all shrink-0"
          >
            <span>Proceed to Next Day</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      )}

      {/* Problems List */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between px-1">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300">
            Assigned Questions ({problems.length})
          </h2>
          <span className="text-xs text-slate-400">
            {completedToday} of {totalToday} completed
          </span>
        </div>

        {problems.length > 0 ? (
          <div className="flex flex-col gap-4">
            {problems.map((prob, idx) => (
              <div key={prob.id || idx} className="relative">
                <div className="absolute -left-2 top-4 w-1 h-8 bg-brand-500 rounded-full hidden sm:block" />
                <ProblemCard
                  problem={prob}
                  onStatusChange={handleStatusChange}
                />
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center flex flex-col items-center gap-4">
            <BookOpen className="w-10 h-10 text-slate-500" />
            <div className="flex flex-col gap-1">
              <span className="text-lg font-bold text-white">No Active Problems for Today</span>
              <span className="text-xs text-slate-400">
                You're either on a scheduled revision day or have completed this week's active questions.
              </span>
            </div>
            <Link
              to="/revision"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl transition-all"
            >
              <span>Check Due Revisions</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};
