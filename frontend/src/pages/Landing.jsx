import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Upload, 
  Sparkles, 
  ArrowRight, 
  Layers, 
  BrainCircuit, 
  CheckCircle2, 
  BarChart3, 
  RotateCcw,
  BookOpen,
  Calendar,
  Compass,
  FileText
} from 'lucide-react';
import { useDSAStore } from '../store/useDSAStore';

export const Landing = () => {
  const { setUseBuiltIn } = useDSAStore();

  const steps = [
    { num: '01', title: 'Upload', desc: 'PDF, DOCX, TXT or CSV LeetCode sheet', icon: Upload },
    { num: '02', title: 'Analyze', desc: 'Classify topics, difficulties & prerequisites', icon: BrainCircuit },
    { num: '03', title: 'Personalize', desc: 'Choose beginner, average or advanced pace', icon: Layers },
    { num: '04', title: 'Practice', desc: 'Day-by-day structured problems with similar concepts', icon: CheckCircle2 },
    { num: '05', title: 'Track Progress', desc: 'Spaced repetition (Day 2/7/21) & weak topic insights', icon: BarChart3 },
  ];

  const highlights = [
    {
      title: 'Prerequisite-Aware Ordering',
      desc: 'Learn Arrays & Hashing before Trees and Graphs. Master Subsets before Dynamic Programming.',
      icon: Compass,
      color: 'text-indigo-400'
    },
    {
      title: 'Similar Concept Links',
      desc: 'Understand that Jump Game is Greedy Reachability, and Single-Threaded CPU is Shortest Job First.',
      icon: Sparkles,
      color: 'text-amber-400'
    },
    {
      title: 'Spaced Repetition Scheduler',
      desc: 'Reinforce problems on Day 2, Day 7, and Day 21 so you never forget patterns before technical interviews.',
      icon: RotateCcw,
      color: 'text-purple-400'
    },
    {
      title: 'Weak Topic Detection',
      desc: 'Automatically identifies topics where you struggle and suggests targeted reinforcement questions.',
      icon: BarChart3,
      color: 'text-emerald-400'
    }
  ];

  return (
    <div className="flex flex-col gap-16 sm:gap-24 py-8 sm:py-16">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto px-4 sm:px-6 flex flex-col items-center gap-6">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-semibold tracking-wide">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Next-Generation DSA Preparation Engine</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight leading-[1.15]">
          Build Your Personalized <br />
          <span className="bg-gradient-to-r from-brand-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
            DSA Roadmap
          </span>
        </h1>

        <p className="text-base sm:text-xl text-slate-300 max-w-2xl font-normal leading-relaxed">
          Upload your DSA sheet, choose your preparation duration and let AI organize the right problems for you.
        </p>

        {/* Call to Actions */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Link
            to="/upload"
            className="inline-flex items-center gap-2 bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-semibold px-6 py-3.5 rounded-xl shadow-lg shadow-brand-500/25 hover:shadow-brand-500/40 hover:scale-[1.02] transition-all duration-200"
          >
            <Upload className="w-4 h-4" />
            <span>Upload DSA Sheet</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </Link>

          <Link
            to="/configure"
            className="inline-flex items-center gap-2 bg-slate-800/90 hover:bg-slate-700/90 text-white font-semibold px-6 py-3.5 rounded-xl border border-slate-700 hover:border-slate-600 transition-all duration-200"
          >
            <Calendar className="w-4 h-4 text-brand-400" />
            <span>Create Roadmap</span>
          </Link>
        </div>

        {/* Fallback Banner for Built-in Dataset */}
        <div className="mt-4 p-3 px-5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 flex items-center gap-3">
          <BookOpen className="w-4 h-4 text-indigo-400 shrink-0" />
          <span>Don't have a DSA sheet?</span>
          <Link
            to="/configure"
            onClick={() => setUseBuiltIn(true)}
            className="text-brand-400 hover:text-brand-300 font-semibold underline underline-offset-4"
          >
            Use Built-in DSA Problem Set (150+ Problems) →
          </Link>
        </div>
      </section>

      {/* 5-Step Process Flow (Section 4 requirement: Upload → Analyze → Personalize → Practice → Track Progress) */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 w-full">
        <div className="text-center mb-10">
          <h2 className="text-xs font-bold uppercase tracking-widest text-brand-400 mb-2">
            The 5-Step Blueprint
          </h2>
          <p className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            How DSA Roadmap AI Transforms Your Preparation
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {steps.map((step, idx) => {
            const Icon = step.icon;
            return (
              <div
                key={step.num}
                className="relative bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 flex flex-col justify-between gap-4 group hover:border-brand-500/40 transition-all duration-200"
              >
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-black text-slate-700 group-hover:text-brand-400 transition-colors">
                    {step.num}
                  </span>
                  <div className="p-2 rounded-lg bg-slate-800 text-brand-400 group-hover:scale-110 transition-transform">
                    <Icon className="w-4 h-4" />
                  </div>
                </div>

                <div>
                  <h3 className="text-base font-bold text-white mb-1">
                    {step.title}
                  </h3>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    {step.desc}
                  </p>
                </div>

                {idx < steps.length - 1 && (
                  <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 z-10 text-slate-700">
                    <ArrowRight className="w-4 h-4" />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* Core Features Grid */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 w-full">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {highlights.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex items-start gap-4 hover:border-slate-700 transition-colors"
              >
                <div className={`p-3 rounded-xl bg-slate-800/80 border border-slate-700/60 shrink-0 ${item.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div className="flex flex-col gap-1.5">
                  <h3 className="text-lg font-bold text-white tracking-tight">
                    {item.title}
                  </h3>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    {item.desc}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
};
