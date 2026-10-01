import React, { useState } from 'react';
import { 
  ExternalLink, 
  CheckCircle2, 
  Clock, 
  HelpCircle, 
  Sparkles, 
  FileText, 
  ChevronDown, 
  ChevronUp,
  Tag,
  Search
} from 'lucide-react';
import { dsaApi } from '../services/api';

export const ProblemCard = ({ 
  problem, 
  onStatusChange, 
  compact = false,
  showNotes = true 
}) => {
  const [status, setStatus] = useState(problem.status || 'Not Started');
  const [isUpdating, setIsUpdating] = useState(false);
  const [notesExpanded, setNotesExpanded] = useState(false);
  const [noteText, setNoteText] = useState(problem.notes || '');

  const lcNum = problem.leetcode_number;
  const title = problem.title || 'Untitled Problem';
  const difficulty = (problem.difficulty || 'Medium').capitalize ? problem.difficulty.capitalize() : problem.difficulty;
  const topic = problem.topic || (problem.topics && problem.topics[0]) || 'General';
  const similarConcept = problem.similar_concept || (problem.similar_problems && problem.similar_problems[0]);
  const slug = problem.slug;
  const itemId = problem.roadmap_item_id || problem.id;

  const leetcodeUrl = dsaApi.getLeetCodeUrl(lcNum, slug, title);

  const getDifficultyStyles = (diff) => {
    switch (diff?.toLowerCase()) {
      case 'easy':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'hard':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      case 'medium':
      default:
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    }
  };

  const getStatusStyles = (stat) => {
    switch (stat) {
      case 'Completed':
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
      case 'In Progress':
        return 'bg-blue-500/20 text-blue-300 border-blue-500/40';
      case 'Skipped':
        return 'bg-slate-700/50 text-slate-400 border-slate-600/40';
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  const handleStatusSelect = async (newStatus) => {
    if (newStatus === status) return;
    setStatus(newStatus);
    if (!itemId) return;

    setIsUpdating(true);
    try {
      await dsaApi.updateProblemStatus(itemId, newStatus, noteText);
      if (onStatusChange) {
        onStatusChange(itemId, newStatus);
      }
    } catch (err) {
      console.error('Failed to update status:', err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleSaveNotes = async () => {
    if (!itemId) return;
    try {
      await dsaApi.updateProblemStatus(itemId, status, noteText);
    } catch (err) {
      console.error('Failed to save notes:', err);
    }
  };

  return (
    <div className={`rounded-xl border transition-all duration-200 ${
      status === 'Completed'
        ? 'bg-slate-900/60 border-emerald-900/40 hover:border-emerald-700/50'
        : 'bg-slate-900/90 border-slate-800 hover:border-slate-700 shadow-sm'
    } p-4 sm:p-5 flex flex-col justify-between gap-3`}>
      {/* Header: LeetCode Number + Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div className="flex items-start sm:items-center gap-2.5">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-base sm:text-lg font-bold text-white tracking-tight">
              {lcNum ? `${lcNum} — ${title}` : title}
            </span>
          </div>
        </div>

        {/* Badges */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getDifficultyStyles(difficulty)}`}>
            {difficulty}
          </span>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">
            {topic}
          </span>
          {problem.estimated_minutes && (
            <span className="hidden sm:flex items-center gap-1 text-slate-400 text-xs">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              {problem.estimated_minutes}m
            </span>
          )}
        </div>
      </div>

      {/* Similar Concept Tag (Section 11 requirement) */}
      {similarConcept && (
        <div className="flex items-center gap-2 bg-indigo-950/40 border border-indigo-800/40 px-3 py-1.5 rounded-lg text-xs text-indigo-300">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
          <span className="font-medium">
            Similar to <span className="text-indigo-200 font-semibold">{similarConcept}</span>
          </span>
        </div>
      )}

      {/* Prerequisites if present */}
      {problem.prerequisites && problem.prerequisites.length > 0 && !compact && (
        <div className="text-xs text-slate-400 flex items-center gap-1.5">
          <span className="text-slate-400">Prerequisites:</span>
          <span>{problem.prerequisites.join(', ')}</span>
        </div>
      )}

      {/* Action Row */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-800/70">
        {/* LeetCode Link */}
        <a
          href={leetcodeUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-400 hover:text-brand-300 bg-brand-500/10 hover:bg-brand-500/20 border border-brand-500/30 px-3 py-1.5 rounded-lg transition-colors"
        >
          {slug ? <ExternalLink className="w-3.5 h-3.5" /> : <Search className="w-3.5 h-3.5" />}
          {slug ? 'Open LeetCode' : 'Search LeetCode'}
        </a>

        {/* Status Switcher Buttons */}
        <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800">
          {['Not Started', 'In Progress', 'Completed', 'Skipped'].map((opt) => (
            <button
              key={opt}
              onClick={() => handleStatusSelect(opt)}
              disabled={isUpdating}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                status === opt
                  ? opt === 'Completed'
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : opt === 'In Progress'
                    ? 'bg-blue-600 text-white'
                    : opt === 'Skipped'
                    ? 'bg-slate-700 text-slate-200'
                    : 'bg-slate-800 text-slate-200'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              {opt === 'Completed' && <CheckCircle2 className="w-3 h-3 inline mr-1" />}
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Optional User Notes */}
      {showNotes && (
        <div className="pt-1">
          <button
            onClick={() => setNotesExpanded(!notesExpanded)}
            className="flex items-center gap-1 text-xs text-slate-400 hover:text-slate-300 transition-colors"
          >
            <FileText className="w-3 h-3" />
            {notesExpanded ? 'Hide Notes' : noteText ? 'View / Edit Notes' : '+ Add Note'}
            {notesExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>

          {notesExpanded && (
            <div className="mt-2 flex flex-col gap-2">
              <textarea
                value={noteText}
                onChange={(e) => setNoteText(e.target.value)}
                placeholder="Write key intuition, time complexity, or edge cases here..."
                rows={2}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-brand-500 transition-colors resize-none"
              />
              <div className="flex justify-end">
                <button
                  onClick={handleSaveNotes}
                  className="px-3 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 rounded-md transition-colors"
                >
                  Save Note
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
