import React, { useState, useMemo } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  CheckCircle2, 
  Search, 
  Filter, 
  ArrowRight, 
  RotateCcw, 
  Sparkles,
  ExternalLink,
  Layers,
  BookOpen
} from 'lucide-react';
import { useDSAStore } from '../store/useDSAStore';
import { ProblemCard } from '../components/ProblemCard';
import { StatsCard } from '../components/StatsCard';

export const PreviewProblems = () => {
  const navigate = useNavigate();
  const { importedProblems, uploadMeta } = useDSAStore();

  const [search, setSearch] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('All');
  const [selectedDiff, setSelectedDiff] = useState('All');

  // If no problems imported, fallback to instructions
  if (!importedProblems || importedProblems.length === 0) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center flex flex-col items-center gap-6">
        <div className="p-4 rounded-2xl bg-slate-800 text-slate-400">
          <BookOpen className="w-10 h-10" />
        </div>
        <div className="flex flex-col gap-2">
          <h2 className="text-2xl font-bold text-white">No Problems Imported Yet</h2>
          <p className="text-sm text-slate-400">
            Upload your DSA sheet or load the built-in problem set to preview and configure your roadmap.
          </p>
        </div>
        <Link
          to="/upload"
          className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-500 text-white font-semibold px-5 py-2.5 rounded-xl shadow-md transition-all"
        >
          <span>Go to Upload Page</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  // Calculate statistics
  const stats = useMemo(() => {
    let easy = 0, medium = 0, hard = 0;
    const topicSet = new Set();

    importedProblems.forEach((p) => {
      const diff = (p.difficulty || 'Medium').toLowerCase();
      if (diff === 'easy') easy++;
      else if (diff === 'hard') hard++;
      else medium++;

      if (p.topics && Array.isArray(p.topics)) {
        p.topics.forEach((t) => topicSet.add(t));
      } else if (p.topic) {
        topicSet.add(p.topic);
      }
    });

    return {
      total: importedProblems.length,
      easy,
      medium,
      hard,
      topics: Array.from(topicSet).sort(),
    };
  }, [importedProblems]);

  // Filtered problems list
  const filteredProblems = useMemo(() => {
    return importedProblems.filter((p) => {
      const title = (p.title || '').toLowerCase();
      const numStr = String(p.leetcode_number || '');
      const concept = (p.similar_concept || '').toLowerCase();
      const query = search.toLowerCase();

      const matchesSearch = !search || title.includes(query) || numStr.includes(query) || concept.includes(query);
      
      const pDiff = (p.difficulty || 'Medium').toLowerCase();
      const matchesDiff = selectedDiff === 'All' || pDiff === selectedDiff.toLowerCase();

      const pTopics = (p.topics || [p.topic || 'General']).map((t) => t.toLowerCase());
      const matchesTopic = selectedTopic === 'All' || pTopics.includes(selectedTopic.toLowerCase());

      return matchesSearch && matchesDiff && matchesTopic;
    });
  }, [importedProblems, search, selectedTopic, selectedDiff]);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-10 flex flex-col gap-8">
      {/* Top Banner & Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Successfully Imported
            </span>
            {uploadMeta?.filename && (
              <span className="text-xs text-slate-400">
                Source: <strong className="text-slate-200">{uploadMeta.filename}</strong>
              </span>
            )}
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Preview Imported Problems ({stats.total})
          </h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Review the extracted LeetCode problems, difficulties and detected algorithm concepts before generating your roadmap.
          </p>
        </div>

        <button
          onClick={() => navigate('/configure')}
          className="inline-flex items-center justify-center gap-2 bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-bold px-6 py-3 rounded-xl shadow-lg shadow-brand-500/20 hover:scale-[1.02] transition-all shrink-0"
        >
          <span>Configure Roadmap</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <StatsCard
          title="Total Questions"
          value={stats.total}
          subtitle={`${stats.topics.length} Unique Topics`}
          color="brand"
        />
        <StatsCard
          title="Easy"
          value={stats.easy}
          subtitle={`${Math.round((stats.easy / stats.total) * 100)}% of Sheet`}
          color="emerald"
        />
        <StatsCard
          title="Medium"
          value={stats.medium}
          subtitle={`${Math.round((stats.medium / stats.total) * 100)}% of Sheet`}
          color="amber"
        />
        <StatsCard
          title="Hard"
          value={stats.hard}
          subtitle={`${Math.round((stats.hard / stats.total) * 100)}% of Sheet`}
          color="rose"
        />
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by LeetCode #, title, or concept..."
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>

        {/* Topic Filter */}
        <div className="flex items-center gap-2">
          <select
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs sm:text-sm text-slate-200 focus:outline-none focus:border-brand-500"
          >
            <option value="All">All Topics ({stats.topics.length})</option>
            {stats.topics.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>

          {/* Difficulty Filter */}
          <select
            value={selectedDiff}
            onChange={(e) => setSelectedDiff(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs sm:text-sm text-slate-200 focus:outline-none focus:border-brand-500"
          >
            <option value="All">All Difficulties</option>
            <option value="Easy">Easy ({stats.easy})</option>
            <option value="Medium">Medium ({stats.medium})</option>
            <option value="Hard">Hard ({stats.hard})</option>
          </select>
        </div>
      </div>

      {/* Problem Cards Grid */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between text-xs text-slate-400 px-1">
          <span>Showing {filteredProblems.length} of {stats.total} problems</span>
          <button
            onClick={() => { setSearch(''); setSelectedTopic('All'); setSelectedDiff('All'); }}
            className="hover:text-brand-400 underline underline-offset-2"
          >
            Reset Filters
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
          {filteredProblems.map((problem, idx) => (
            <ProblemCard 
              key={problem.id || problem.leetcode_number || idx} 
              problem={problem} 
              showNotes={false}
            />
          ))}
        </div>
      </div>

      {/* Bottom Floating Action Bar */}
      <div className="sticky bottom-4 z-40 bg-slate-900/95 backdrop-blur-md border border-slate-700/80 p-4 rounded-2xl shadow-xl flex items-center justify-between gap-4">
        <div>
          <span className="text-sm font-bold text-white block">
            Ready to generate your custom schedule?
          </span>
          <span className="text-xs text-slate-400">
            {stats.total} problems loaded • Prerequisite DAG active
          </span>
        </div>

        <button
          onClick={() => navigate('/configure')}
          className="inline-flex items-center gap-2 bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-bold px-6 py-2.5 rounded-xl shadow-md transition-all shrink-0"
        >
          <span>Continue to Configure</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
