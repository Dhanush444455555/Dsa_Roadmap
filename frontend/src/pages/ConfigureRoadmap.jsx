import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  Calendar, 
  Target, 
  Brain, 
  CheckCircle2, 
  Loader2, 
  ArrowRight,
  Layers,
  Award,
  Zap
} from 'lucide-react';
import { dsaApi } from '../services/api';
import { useDSAStore } from '../store/useDSAStore';

export const ConfigureRoadmap = () => {
  const navigate = useNavigate();
  const { 
    importedProblems, 
    userLevel, 
    setUserLevel, 
    durationMonths, 
    setDurationMonths, 
    targetProblemCount, 
    setTargetProblemCount,
    roadmapTitle,
    setRoadmapTitle,
    useBuiltIn,
    setActiveRoadmap 
  } = useDSAStore();

  const [customDuration, setCustomDuration] = useState('');
  const [customProblemCount, setCustomProblemCount] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const levels = [
    {
      id: 'Beginner',
      title: 'Beginner',
      tagline: 'Foundations First',
      desc: 'Starts with high volume of Easy problems, gradual intro to Mediums. Focus on syntax & fundamental data structures.',
      ratio: '65% Easy • 35% Medium',
      icon: Brain,
      color: 'border-emerald-500/40 text-emerald-400 bg-emerald-500/10'
    },
    {
      id: 'Average',
      title: 'Average',
      tagline: 'Standard Interview Prep',
      desc: 'Balanced progression from Easy to Medium, ending with select Hard questions. Ideal for general software engineering interviews.',
      ratio: '25% Easy • 60% Medium • 15% Hard',
      icon: Zap,
      color: 'border-brand-500/40 text-brand-400 bg-brand-500/10'
    },
    {
      id: 'Advanced',
      title: 'Advanced',
      tagline: 'FAANG / Competitive Focus',
      desc: 'Fast-paced schedule emphasizing complex Mediums, advanced graph algorithms, and competitive Hard DP problems.',
      ratio: '10% Easy • 55% Medium • 35% Hard',
      icon: Award,
      color: 'border-purple-500/40 text-purple-400 bg-purple-500/10'
    }
  ];

  const durationOptions = [3, 6, 9, 12];
  const problemOptions = [20, 50, 100, 150, 200];

  const handleGenerate = async () => {
    setErrorMsg('');
    setIsGenerating(true);

    const finalDuration = customDuration ? parseInt(customDuration) : durationMonths;
    const finalCount = customProblemCount ? parseInt(customProblemCount) : targetProblemCount;

    if (!finalDuration || finalDuration <= 0) {
      setErrorMsg('Please specify a valid duration in months.');
      setIsGenerating(false);
      return;
    }

    if (!finalCount || finalCount <= 0) {
      setErrorMsg('Please specify a valid target problem count.');
      setIsGenerating(false);
      return;
    }

    try {
      const payload = {
        user_level: userLevel,
        duration_months: finalDuration,
        target_problem_count: finalCount,
        title: roadmapTitle || `${userLevel} ${finalDuration}-Month DSA Roadmap`,
        problems: importedProblems && importedProblems.length > 0 ? importedProblems : null,
        use_built_in: useBuiltIn || (!importedProblems || importedProblems.length === 0)
      };

      const result = await dsaApi.generateRoadmap(payload);
      setActiveRoadmap(result);
      navigate('/roadmap');
    } catch (err) {
      console.error(err);
      setErrorMsg(err.response?.data?.detail || 'Failed to generate roadmap. Please check configuration.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col gap-10">
      {/* Header */}
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
          Configure Your Personalized Roadmap
        </h1>
        <p className="text-sm sm:text-base text-slate-300">
          Tailor the generation algorithm to match your target timeline, problem capacity, and current proficiency level.
        </p>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm">
          {errorMsg}
        </div>
      )}

      {/* 1. Current DSA Level (Section 7 requirement) */}
      <div className="flex flex-col gap-3">
        <label className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <Brain className="w-4 h-4 text-brand-400" />
          <span>1. Select Current DSA Level</span>
        </label>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {levels.map((lvl) => {
            const Icon = lvl.icon;
            const isSelected = userLevel === lvl.id;
            return (
              <div
                key={lvl.id}
                onClick={() => setUserLevel(lvl.id)}
                className={`rounded-2xl p-5 border cursor-pointer transition-all duration-200 flex flex-col justify-between gap-3 ${
                  isSelected
                    ? 'bg-slate-900 border-brand-500 shadow-lg shadow-brand-500/10 ring-1 ring-brand-500'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className={`p-2.5 rounded-xl border ${lvl.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  {isSelected && (
                    <CheckCircle2 className="w-5 h-5 text-brand-400" />
                  )}
                </div>

                <div>
                  <h3 className="text-base font-bold text-white mb-0.5">
                    {lvl.title}
                  </h3>
                  <span className="text-xs text-brand-400 font-semibold block mb-1.5">
                    {lvl.tagline}
                  </span>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    {lvl.desc}
                  </p>
                </div>

                <div className="pt-2 border-t border-slate-800/80">
                  <span className="text-[11px] font-semibold text-slate-300">
                    Difficulty Mix: {lvl.ratio}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 2. Preparation Duration (Section 7 requirement) */}
      <div className="flex flex-col gap-3">
        <label className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <Calendar className="w-4 h-4 text-indigo-400" />
          <span>2. Preparation Duration</span>
        </label>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          {durationOptions.map((m) => (
            <button
              key={m}
              onClick={() => { setDurationMonths(m); setCustomDuration(''); }}
              className={`p-3.5 rounded-xl text-center font-bold text-sm border transition-all ${
                durationMonths === m && !customDuration
                  ? 'bg-brand-600 text-white border-brand-500 shadow-md'
                  : 'bg-slate-900/80 text-slate-300 border-slate-800 hover:border-slate-700'
              }`}
            >
              {m} Months
            </button>
          ))}

          <input
            type="number"
            value={customDuration}
            onChange={(e) => { setCustomDuration(e.target.value); if (e.target.value) setDurationMonths(parseInt(e.target.value)); }}
            placeholder="Custom (Mo)"
            min={1}
            max={24}
            className={`p-3 rounded-xl text-center text-xs font-semibold bg-slate-950 border focus:outline-none ${
              customDuration ? 'border-brand-500 text-brand-400' : 'border-slate-800 text-slate-300'
            }`}
          />
        </div>
      </div>

      {/* 3. Number of Problems (Section 7 requirement) */}
      <div className="flex flex-col gap-3">
        <label className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <Target className="w-4 h-4 text-emerald-400" />
          <span>3. Target Problem Count</span>
        </label>

        <div className="grid grid-cols-2 sm:grid-cols-6 gap-3">
          {problemOptions.map((c) => (
            <button
              key={c}
              onClick={() => { setTargetProblemCount(c); setCustomProblemCount(''); }}
              className={`p-3.5 rounded-xl text-center font-bold text-sm border transition-all ${
                targetProblemCount === c && !customProblemCount
                  ? 'bg-emerald-600 text-white border-emerald-500 shadow-md'
                  : 'bg-slate-900/80 text-slate-300 border-slate-800 hover:border-slate-700'
              }`}
            >
              {c} Problems
            </button>
          ))}

          <input
            type="number"
            value={customProblemCount}
            onChange={(e) => { setCustomProblemCount(e.target.value); if (e.target.value) setTargetProblemCount(parseInt(e.target.value)); }}
            placeholder="Custom #"
            min={5}
            max={500}
            className={`p-3 rounded-xl text-center text-xs font-semibold bg-slate-950 border focus:outline-none ${
              customProblemCount ? 'border-emerald-500 text-emerald-400' : 'border-slate-800 text-slate-300'
            }`}
          />
        </div>
      </div>

      {/* Roadmap Title */}
      <div className="flex flex-col gap-2">
        <label className="text-xs font-semibold text-slate-400">
          Roadmap Title (Optional):
        </label>
        <input
          type="text"
          value={roadmapTitle}
          onChange={(e) => setRoadmapTitle(e.target.value)}
          placeholder="e.g. My 6-Month FAANG Preparation Schedule"
          className="bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-slate-100 focus:outline-none focus:border-brand-500"
        />
      </div>

      {/* Action Button */}
      <div className="pt-4 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-xs text-slate-400">
          {importedProblems && importedProblems.length > 0 ? (
            <span>Using <strong>{importedProblems.length}</strong> imported problems from your sheet.</span>
          ) : (
            <span>Using <strong>Built-in DSA Problem Set (150+ problems)</strong>.</span>
          )}
        </div>

        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-gradient-to-r from-brand-600 via-indigo-600 to-purple-600 hover:from-brand-500 hover:to-purple-500 text-white font-bold px-8 py-4 rounded-xl shadow-xl shadow-brand-500/20 hover:scale-[1.02] transition-all"
        >
          {isGenerating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Generating Intelligent Roadmap...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              <span>Generate Personalized Roadmap</span>
              <ArrowRight className="w-5 h-5 ml-1" />
            </>
          )}
        </button>
      </div>
    </div>
  );
};
