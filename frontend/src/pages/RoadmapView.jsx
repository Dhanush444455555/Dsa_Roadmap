import React, { useEffect, useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { 
  Calendar, 
  MapPin, 
  CheckCircle2, 
  ChevronDown, 
  ChevronUp, 
  Sparkles, 
  Search, 
  Filter, 
  Download, 
  Loader2,
  Clock,
  Layers,
  ArrowRight,
  BookOpen
} from 'lucide-react';
import { dsaApi } from '../services/api';
import { useDSAStore } from '../store/useDSAStore';
import { ProblemCard } from '../components/ProblemCard';
import { ProgressBar } from '../components/ProgressBar';

export const RoadmapView = () => {
  const { activeRoadmap, setActiveRoadmap, updateLocalItemStatus } = useDSAStore();
  const [isLoading, setIsLoading] = useState(false);
  const [selectedMonth, setSelectedMonth] = useState('All');
  const [expandedWeeks, setExpandedWeeks] = useState({ 1: true });
  const [searchTerm, setSearchTerm] = useState('');
  const [diffFilter, setDiffFilter] = useState('All');

  useEffect(() => {
    if (!activeRoadmap) {
      setIsLoading(true);
      dsaApi.getCurrentRoadmap()
        .then((data) => {
          if (data) setActiveRoadmap(data);
        })
        .catch((err) => console.error(err))
        .finally(() => setIsLoading(false));
    }
  }, [activeRoadmap, setActiveRoadmap]);

  const toggleWeek = (weekNum) => {
    setExpandedWeeks((prev) => ({
      ...prev,
      [weekNum]: !prev[weekNum]
    }));
  };

  const expandAllWeeks = () => {
    if (!activeRoadmap?.weeks) return;
    const all = {};
    activeRoadmap.weeks.forEach((w) => { all[w.week] = true; });
    setExpandedWeeks(all);
  };

  const collapseAllWeeks = () => {
    setExpandedWeeks({});
  };

  // Calculate overall roadmap progress
  const progressStats = useMemo(() => {
    if (!activeRoadmap?.weeks) return { total: 0, completed: 0, percentage: 0 };
    let total = 0;
    let completed = 0;

    activeRoadmap.weeks.forEach((week) => {
      week.days.forEach((day) => {
        day.problems.forEach((prob) => {
          total++;
          if (prob.status === 'Completed') completed++;
        });
      });
    });

    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    return { total, completed, percentage: pct };
  }, [activeRoadmap]);

  // Export roadmap as JSON
  const handleExportJSON = () => {
    if (!activeRoadmap) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(activeRoadmap, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `DSA_Roadmap_${activeRoadmap.user_level}_${activeRoadmap.duration_months}Months.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center flex flex-col items-center gap-4">
        <Loader2 className="w-10 h-10 animate-spin text-brand-400" />
        <span className="text-base font-semibold text-slate-300">Loading your personalized roadmap...</span>
      </div>
    );
  }

  if (!activeRoadmap) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center flex flex-col items-center gap-6">
        <div className="p-4 rounded-2xl bg-slate-800 text-slate-400">
          <BookOpen className="w-10 h-10" />
        </div>
        <div className="flex flex-col gap-2">
          <h2 className="text-2xl font-bold text-white">No Roadmap Generated Yet</h2>
          <p className="text-sm text-slate-400">
            Upload your DSA sheet or customize your preferences to generate your personalized roadmap.
          </p>
        </div>
        <Link
          to="/configure"
          className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-500 text-white font-semibold px-5 py-2.5 rounded-xl shadow-md transition-all"
        >
          <span>Configure & Generate Roadmap</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  const { title, user_level, duration_months, total_problems, total_weeks, month_breakdown, weeks } = activeRoadmap;

  // Filter weeks by month or search query
  const filteredWeeks = weeks.filter((w) => {
    const matchesMonth = selectedMonth === 'All' || w.month === parseInt(selectedMonth);
    if (!matchesMonth) return false;

    if (!searchTerm && diffFilter === 'All') return true;

    // Check if any problem matches search or difficulty
    return w.days.some((d) =>
      d.problems.some((p) => {
        const titleMatch = (p.title || '').toLowerCase().includes(searchTerm.toLowerCase());
        const numMatch = String(p.leetcode_number || '').includes(searchTerm);
        const conceptMatch = (p.similar_concept || '').toLowerCase().includes(searchTerm.toLowerCase());
        const diffMatch = diffFilter === 'All' || (p.difficulty || '').toLowerCase() === diffFilter.toLowerCase();
        return (titleMatch || numMatch || conceptMatch) && diffMatch;
      })
    );
  });

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-10 flex flex-col gap-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950/40 border border-slate-800 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-xl">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/30">
              {user_level} Track
            </span>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
              {duration_months} Months • {total_weeks} Weeks
            </span>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              {total_problems} Problems
            </span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {title || 'Personalized DSA Preparation Roadmap'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Prerequisite-ordered roadmap with concept interleaving and spaced revision cycles.
          </p>
        </div>

        {/* Action Button & Export */}
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={handleExportJSON}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 transition-colors shadow-sm"
          >
            <Download className="w-3.5 h-3.5 text-slate-400" />
            Export Plan
          </button>

          <Link
            to="/today"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 text-white text-xs font-bold shadow-md transition-all"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            Go to Today's Tasks
          </Link>
        </div>
      </div>

      {/* Progress Bar Summary */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 sm:p-5 shadow-sm">
        <ProgressBar
          percentage={progressStats.percentage}
          completed={progressStats.completed}
          total={progressStats.total}
          label="Overall Preparation Progress"
          color="brand"
        />
      </div>

      {/* Month Milestones Flow (Section 14 visual roadmap requirement) */}
      {month_breakdown && month_breakdown.length > 0 && (
        <div className="flex flex-col gap-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Monthly Milestone Architecture
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {month_breakdown.map((m) => (
              <div
                key={m.month}
                onClick={() => setSelectedMonth(selectedMonth === String(m.month) ? 'All' : String(m.month))}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  selectedMonth === String(m.month)
                    ? 'bg-slate-900 border-brand-500 shadow-md ring-1 ring-brand-500'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-brand-400">
                    Month {m.month}
                  </span>
                  <span className="text-[11px] text-slate-500 font-medium">
                    Weeks {m.weeks?.join(', ')}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white mb-2">
                  {m.title}
                </h4>
                <div className="flex flex-wrap gap-1">
                  {m.focus_topics?.map((topic, i) => (
                    <span
                      key={i}
                      className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-slate-700/60"
                    >
                      {topic}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter and Accordion Controls */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search problems or concepts in roadmap..."
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>

        {/* Filter Month */}
        <div className="flex items-center gap-2">
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs sm:text-sm text-slate-200 focus:outline-none focus:border-brand-500"
          >
            <option value="All">All Months</option>
            {month_breakdown?.map((m) => (
              <option key={m.month} value={m.month}>Month {m.month}</option>
            ))}
          </select>

          <select
            value={diffFilter}
            onChange={(e) => setDiffFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs sm:text-sm text-slate-200 focus:outline-none focus:border-brand-500"
          >
            <option value="All">All Levels</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>

          {/* Expand/Collapse All */}
          <button
            onClick={expandAllWeeks}
            className="px-2.5 py-2 text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg border border-slate-700 font-medium"
            title="Expand All Weeks"
          >
            Expand All
          </button>
        </div>
      </div>

      {/* Weeks & Days Timeline */}
      <div className="flex flex-col gap-6">
        {filteredWeeks.map((week) => {
          const isExpanded = expandedWeeks[week.week] ?? false;
          const weekProbCount = week.days.reduce((acc, d) => acc + d.problems.length, 0);
          const weekCompletedCount = week.days.reduce((acc, d) => acc + d.problems.filter((p) => p.status === 'Completed').length, 0);
          const weekPct = weekProbCount > 0 ? Math.round((weekCompletedCount / weekProbCount) * 100) : 0;

          return (
            <div
              key={week.week}
              className="bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-sm"
            >
              {/* Week Accordion Header */}
              <div
                onClick={() => toggleWeek(week.week)}
                className="p-4 sm:p-5 bg-slate-900 hover:bg-slate-850 cursor-pointer flex items-center justify-between gap-4 border-b border-slate-800/80 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-brand-500/10 border border-brand-500/30 text-brand-400 font-extrabold flex items-center justify-center text-sm">
                    W{week.week}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-base font-bold text-white">
                        Week {week.week}
                      </h3>
                      <span className="text-xs text-slate-400">
                        (Month {week.month})
                      </span>
                    </div>
                    <div className="flex items-center gap-1.5 flex-wrap mt-0.5">
                      {week.focus.map((f, i) => (
                        <span key={i} className="text-[11px] font-medium text-slate-300 bg-slate-800 px-2 py-0.5 rounded-md border border-slate-700">
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="hidden sm:flex flex-col items-end gap-1 text-xs">
                    <span className="font-semibold text-slate-300">
                      {weekCompletedCount}/{weekProbCount} Solved ({weekPct}%)
                    </span>
                    <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-brand-500 rounded-full transition-all"
                        style={{ width: `${weekPct}%` }}
                      />
                    </div>
                  </div>

                  {isExpanded ? (
                    <ChevronUp className="w-5 h-5 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-slate-400" />
                  )}
                </div>
              </div>

              {/* Week Days List */}
              {isExpanded && (
                <div className="p-4 sm:p-6 flex flex-col gap-6 bg-slate-950/40">
                  {week.days.map((day) => {
                    return (
                      <div
                        key={day.day}
                        className={`rounded-xl p-4 border flex flex-col gap-3 ${
                          day.is_revision
                            ? 'bg-purple-950/20 border-purple-900/30'
                            : 'bg-slate-900/50 border-slate-800/80'
                        }`}
                      >
                        {/* Day Header */}
                        <div className="flex items-center justify-between border-b border-slate-800/70 pb-2">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-white bg-slate-800 px-2.5 py-1 rounded-md border border-slate-700">
                              Day {day.day}
                            </span>
                            <span className="text-xs font-semibold text-slate-300">
                              Focus: <strong className="text-brand-300">{day.focus_topic}</strong>
                            </span>
                          </div>

                          {day.is_revision ? (
                            <span className="text-xs font-semibold text-purple-400 bg-purple-500/10 px-2.5 py-0.5 rounded-full border border-purple-500/20">
                              Revision & Mock Practice Day
                            </span>
                          ) : (
                            <span className="text-xs text-slate-400">
                              {day.problems.length} {day.problems.length === 1 ? 'Problem' : 'Problems'}
                            </span>
                          )}
                        </div>

                        {/* Problems for this day */}
                        {day.problems && day.problems.length > 0 ? (
                          <div className="grid grid-cols-1 gap-3">
                            {day.problems.map((prob, pIdx) => (
                              <ProblemCard
                                key={prob.roadmap_item_id || prob.id || pIdx}
                                problem={prob}
                                onStatusChange={(itemId, newStat) => {
                                  updateLocalItemStatus(itemId, newStat);
                                }}
                              />
                            ))}
                          </div>
                        ) : (
                          <div className="py-3 text-center text-xs text-slate-400 italic">
                            {day.is_revision 
                              ? 'Dedicate today to reviewing past problems on Day 2 / Day 7 intervals, studying time complexities, and mock interviews.'
                              : 'Rest or buffer catch-up day.'}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
