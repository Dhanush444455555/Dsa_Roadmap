import React, { useEffect, useState } from 'react';
import { 
  RotateCcw, 
  CheckCircle2, 
  Calendar, 
  Sparkles, 
  Clock, 
  ExternalLink, 
  AlertCircle, 
  Loader2,
  BookOpen,
  FolderPlus,
  Download,
  Share2,
  Eye,
  X,
  FileText,
  Copy,
  Plus,
  Users
} from 'lucide-react';
import { dsaApi } from '../services/api';

export const RevisionPage = () => {
  const [revisions, setRevisions] = useState([]);
  const [filter, setFilter] = useState('All'); // 'All', 'Pending', 'Completed'
  const [isLoading, setIsLoading] = useState(true);

  // Google Drive Links State
  const [driveLinks, setDriveLinks] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showFormulaModal, setShowFormulaModal] = useState(false);
  const [formulaDoc, setFormulaDoc] = useState(null);
  const [copySuccess, setCopySuccess] = useState(false);

  // New Link Form State
  const [newTitle, setNewTitle] = useState('');
  const [newUrl, setNewUrl] = useState('');
  const [newContributor, setNewContributor] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [isSubmittingLink, setIsSubmittingLink] = useState(false);
  const [formError, setFormError] = useState('');

  const fetchRevisions = () => {
    setIsLoading(true);
    Promise.all([
      dsaApi.getRevisions(filter),
      dsaApi.getDriveLinks()
    ])
      .then(([revData, driveData]) => {
        setRevisions(revData || []);
        setDriveLinks(driveData || []);
      })
      .catch((err) => console.error(err))
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    fetchRevisions();
  }, [filter]);

  const handleMarkRevision = async (revId, status) => {
    try {
      await dsaApi.updateRevisionStatus(revId, status);
      setRevisions((prev) =>
        prev.map((r) => (r.id === revId ? { ...r, status } : r))
      );
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpenFormulaModal = async () => {
    setShowFormulaModal(true);
    if (!formulaDoc) {
      try {
        const data = await dsaApi.getFormulaDoc();
        setFormulaDoc(data);
      } catch (err) {
        console.error(err);
      }
    }
  };

  const handleAddDriveLink = async (e) => {
    e.preventDefault();
    if (!newUrl.trim()) {
      setFormError('Please provide a Google Drive URL.');
      return;
    }
    if (!newUrl.includes('drive.google.com') && !newUrl.includes('docs.google.com') && !newUrl.includes('http')) {
      setFormError('Please enter a valid Google Drive folder or document URL.');
      return;
    }

    setIsSubmittingLink(true);
    setFormError('');

    try {
      const added = await dsaApi.addDriveLink({
        title: newTitle || 'Community DSA Google Drive Folder',
        drive_url: newUrl,
        contributor: newContributor || 'Anonymous',
        description: newDescription || 'Shared DSA preparation folder with formulas and cheat sheets.',
        category: 'Formula Sheet & Notes'
      });
      setDriveLinks([added, ...driveLinks]);
      setShowAddModal(false);
      setNewTitle('');
      setNewUrl('');
      setNewContributor('');
      setNewDescription('');
    } catch (err) {
      console.error(err);
      setFormError('Failed to save Google Drive link.');
    } finally {
      setIsSubmittingLink(false);
    }
  };

  const handleCopyLink = (url) => {
    navigator.clipboard.writeText(url);
    setCopySuccess(true);
    setTimeout(() => setCopySuccess(false), 2000);
  };

  const dueTodayItems = revisions.filter((r) => r.is_due_today && r.status === 'Pending');
  const overdueItems = revisions.filter((r) => r.is_overdue && r.status === 'Pending');
  const upcomingItems = revisions.filter((r) => !r.is_due_today && !r.is_overdue && r.status === 'Pending');

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center flex flex-col items-center gap-4">
        <Loader2 className="w-10 h-10 animate-spin text-purple-400" />
        <span className="text-base font-semibold text-slate-300">Loading revision schedule & Google Drive resources...</span>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col gap-10">
      {/* Page Header */}
      <div className="bg-gradient-to-r from-purple-950/40 via-slate-900 to-indigo-950/40 border border-purple-500/30 rounded-2xl p-6 sm:p-8 flex flex-col sm:flex-row sm:items-center justify-between gap-6 shadow-xl">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
              Revision & Formula Hub
            </span>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              Shared Drive Integration
            </span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
            Formulas, Drive Hub & Revisions
          </h1>
          <p className="text-xs sm:text-sm text-slate-300">
            Access our master formulas document, upload/browse shared Google Drive folders, and review spaced repetition problems (Day 2 → Day 7 → Day 21).
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setFilter('All')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              filter === 'All' ? 'bg-purple-600 text-white shadow-md' : 'bg-slate-800 text-slate-300'
            }`}
          >
            All Items
          </button>
          <button
            onClick={() => setFilter('Pending')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              filter === 'Pending' ? 'bg-purple-600 text-white shadow-md' : 'bg-slate-800 text-slate-300'
            }`}
          >
            Pending
          </button>
        </div>
      </div>

      {/* ============================================================== */}
      {/* 1. MASTER FORMULAS & TRICKS DOC + GOOGLE DRIVE REPOSITORY HUB */}
      {/* ============================================================== */}
      <section className="bg-gradient-to-br from-indigo-950/30 via-slate-900 to-slate-950 border border-indigo-500/30 rounded-2xl p-6 sm:p-8 flex flex-col gap-6 shadow-xl">
        {/* Section Top Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
          <div className="flex items-start sm:items-center gap-3">
            <div className="p-3 rounded-2xl bg-indigo-500/20 border border-indigo-500/40 text-indigo-400 shrink-0">
              <Share2 className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
                DSA Formulas & Google Drive Folder Hub
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                  Ready to Share
                </span>
              </h2>
              <p className="text-xs sm:text-sm text-slate-300">
                Created master document with all formulas and tricks. Download it below or upload/browse shared Google Drive folders!
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2.5 shrink-0 flex-wrap">
            <button
              onClick={() => setShowAddModal(true)}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white text-xs font-bold shadow-md transition-all"
            >
              <FolderPlus className="w-4 h-4" />
              Upload Google Drive Link
            </button>
          </div>
        </div>

        {/* Master Formula Doc Showcase Card */}
        <div className="bg-slate-950/80 border border-indigo-500/30 rounded-xl p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20 shrink-0 mt-1">
              <FileText className="w-6 h-6" />
            </div>
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <span className="text-sm sm:text-base font-bold text-white">
                  DSA Formulas, Patterns & Tricks Master Document (.docx)
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  Official Master Doc
                </span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed max-w-2xl">
                Contains complete invariants for Time/Space Complexity rules ($N \le 10 \dots 10^9$), Bitwise tricks, Kadane & Boyer-Moore, Two-Pointer invariants, Sliding Window templates, Safe Binary Search on Answer Space, Monotonic Stacks, Tree LCA/Diameter, Dijkstra & DSU, and 0/1 vs Unbounded DP state transitions.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto shrink-0 flex-wrap">
            <button
              onClick={handleOpenFormulaModal}
              className="flex-1 md:flex-initial inline-flex items-center justify-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 transition-colors"
            >
              <Eye className="w-3.5 h-3.5 text-slate-400" />
              Read in App
            </button>

            <a
              href="/api/download-formula-doc"
              download="DSA_Formulas_and_Tricks_Master.docx"
              className="flex-1 md:flex-initial inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              Download .DOCX
            </a>
          </div>
        </div>

        {/* Community Shared Google Drive Folders List */}
        <div className="flex flex-col gap-3 pt-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5 text-indigo-400" />
              Shared Community Google Drive Folders ({driveLinks.length})
            </span>
            <span className="text-[11px] text-slate-400">
              Upload your own folder or access shared notes
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            {driveLinks.map((link) => (
              <div
                key={link.id}
                className="bg-slate-900/90 border border-slate-800 hover:border-indigo-500/40 rounded-xl p-4 flex flex-col justify-between gap-3 transition-all shadow-sm"
              >
                <div className="flex flex-col gap-1.5">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-indigo-300 border border-slate-700">
                      {link.category || 'Shared Notes'}
                    </span>
                    <span className="text-[11px] text-slate-400">
                      By {link.contributor || 'Community'}
                    </span>
                  </div>

                  <span className="text-sm font-bold text-white line-clamp-1">
                    {link.title}
                  </span>

                  {link.description && (
                    <p className="text-xs text-slate-400 line-clamp-2">
                      {link.description}
                    </p>
                  )}
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
                  <span className="text-[11px] text-slate-400 font-mono truncate max-w-[180px]">
                    {link.drive_url}
                  </span>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleCopyLink(link.drive_url)}
                      className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                      title="Copy Drive Link"
                    >
                      <Copy className="w-3.5 h-3.5" />
                    </button>

                    <a
                      href={link.drive_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600/20 hover:bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 hover:text-indigo-200 text-xs font-semibold rounded-lg transition-colors"
                    >
                      <span>Open in Drive</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================== */}
      {/* 2. SPACED REPETITION PROBLEM ITEMS SCHEDULE */}
      {/* ============================================================== */}

      {/* Due Today Banner (Section 17 requirement: "Problems to Revise Today") */}
      {dueTodayItems.length > 0 && (
        <div className="flex flex-col gap-3">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-purple-400" />
            <h2 className="text-base font-bold text-white uppercase tracking-wider text-xs">
              Problems to Revise Today ({dueTodayItems.length})
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {dueTodayItems.map((item) => (
              <RevisionCard
                key={item.id}
                item={item}
                onComplete={() => handleMarkRevision(item.id, 'Completed')}
                onSkip={() => handleMarkRevision(item.id, 'Skipped')}
              />
            ))}
          </div>
        </div>
      )}

      {/* Overdue Items Banner */}
      {overdueItems.length > 0 && (
        <div className="flex flex-col gap-3">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-400" />
            <h2 className="text-base font-bold text-amber-300 uppercase tracking-wider text-xs">
              Overdue for Revision ({overdueItems.length})
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {overdueItems.map((item) => (
              <RevisionCard
                key={item.id}
                item={item}
                isOverdue={true}
                onComplete={() => handleMarkRevision(item.id, 'Completed')}
                onSkip={() => handleMarkRevision(item.id, 'Skipped')}
              />
            ))}
          </div>
        </div>
      )}

      {/* Upcoming Revisions */}
      <div className="flex flex-col gap-3">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
          Upcoming Spaced Revisions ({upcomingItems.length})
        </h2>

        {upcomingItems.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {upcomingItems.map((item) => (
              <RevisionCard
                key={item.id}
                item={item}
                onComplete={() => handleMarkRevision(item.id, 'Completed')}
                onSkip={() => handleMarkRevision(item.id, 'Skipped')}
              />
            ))}
          </div>
        ) : (
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-10 text-center flex flex-col items-center gap-3">
            <BookOpen className="w-8 h-8 text-slate-500" />
            <span className="text-sm font-semibold text-white">No Pending Revisions in Queue</span>
            <span className="text-xs text-slate-400">
              When you mark problems as "Completed" in your daily tasks or roadmap, they will automatically be scheduled here!
            </span>
          </div>
        )}
      </div>

      {/* ============================================================== */}
      {/* MODAL 1: UPLOAD / SUBMIT GOOGLE DRIVE FOLDER LINK */}
      {/* ============================================================== */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 flex flex-col gap-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <FolderPlus className="w-5 h-5 text-indigo-400" />
                <h3 className="text-lg font-bold text-white">
                  Share Google Drive Folder Link
                </h3>
              </div>
              <button
                onClick={() => setShowAddModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {formError && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs rounded-xl">
                {formError}
              </div>
            )}

            <form onSubmit={handleAddDriveLink} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-semibold text-slate-300">
                  Google Drive Folder or Document URL *
                </label>
                <input
                  type="url"
                  required
                  value={newUrl}
                  onChange={(e) => setNewUrl(e.target.value)}
                  placeholder="https://drive.google.com/drive/folders/..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-semibold text-slate-300">
                  Folder / Resource Title *
                </label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Full-Stack DSA Formula Sheets & Handwritten Notes"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="flex flex-col sm:flex-row gap-3">
                <div className="flex-1 flex flex-col gap-1.5">
                  <label className="text-xs font-semibold text-slate-300">
                    Your Name / Contributor
                  </label>
                  <input
                    type="text"
                    value={newContributor}
                    onChange={(e) => setNewContributor(e.target.value)}
                    placeholder="e.g. Dhanush / Anonymous"
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-brand-500"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-semibold text-slate-300">
                  Description
                </label>
                <textarea
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  placeholder="Describe what formulas, cheat sheets or solutions are inside this drive folder..."
                  rows={3}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-brand-500 resize-none"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-slate-200 bg-slate-800 hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmittingLink}
                  className="inline-flex items-center gap-1.5 px-5 py-2 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 transition-all shadow-md"
                >
                  {isSubmittingLink ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <FolderPlus className="w-3.5 h-3.5" />}
                  Submit Google Drive Link
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* MODAL 2: IN-APP FORMULAS & TRICKS PREVIEW DRAWER */}
      {/* ============================================================== */}
      {showFormulaModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-3xl w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/70">
              <div className="flex items-center gap-2.5">
                <FileText className="w-5 h-5 text-indigo-400" />
                <h3 className="text-base sm:text-lg font-bold text-white">
                  DSA Formulas, Patterns & Tricks Master Document
                </h3>
              </div>
              <div className="flex items-center gap-2">
                <a
                  href="/api/download-formula-doc"
                  download="DSA_Formulas_and_Tricks_Master.docx"
                  className="inline-flex items-center gap-1 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg shadow-sm"
                >
                  <Download className="w-3 h-3" />
                  Download .DOCX
                </a>
                <button
                  onClick={() => setShowFormulaModal(false)}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-6 text-sm text-slate-200 leading-relaxed font-sans">
              <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/20 text-xs text-indigo-300">
                Tip: Download this document in Word format (.docx) using the button above and upload it to your Google Drive folder for anytime offline mobile reference!
              </div>

              {formulaDoc ? (
                <div className="whitespace-pre-wrap font-mono text-xs text-slate-300 bg-slate-950 p-4 rounded-xl border border-slate-800/80 leading-5">
                  {formulaDoc.content}
                </div>
              ) : (
                <div className="py-12 text-center flex flex-col items-center gap-3">
                  <Loader2 className="w-6 h-6 animate-spin text-indigo-400" />
                  <span className="text-xs text-slate-400">Loading master formula document...</span>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-slate-800 bg-slate-950 flex items-center justify-between">
              <span className="text-xs text-slate-400">
                Created for technical interviews & fast revision
              </span>
              <button
                onClick={() => setShowFormulaModal(false)}
                className="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200"
              >
                Close Preview
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const RevisionCard = ({ item, isOverdue = false, onComplete, onSkip }) => {
  const leetcodeUrl = dsaApi.getLeetCodeUrl(item.leetcode_number, '', item.title);

  return (
    <div className={`p-4 rounded-xl border transition-all flex flex-col justify-between gap-3 ${
      item.status === 'Completed'
        ? 'bg-slate-900/40 border-slate-800 opacity-70'
        : isOverdue
        ? 'bg-amber-950/20 border-amber-500/40'
        : 'bg-slate-900/80 border-slate-800 hover:border-slate-700 shadow-sm'
    }`}>
      <div className="flex flex-col gap-1.5">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/20">
              Day {item.interval_day} Interval
            </span>
            <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
              {item.topic}
            </span>
          </div>

          <span className="text-[11px] text-slate-400">
            Due: {item.due_date}
          </span>
        </div>

        <span className="text-sm font-bold text-white">
          {item.leetcode_number ? `${item.leetcode_number} — ` : ''}{item.title}
        </span>

        {item.similar_concept && (
          <span className="text-xs text-indigo-300">
            Pattern: {item.similar_concept}
          </span>
        )}
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
        <a
          href={leetcodeUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs font-semibold text-brand-400 hover:text-brand-300 inline-flex items-center gap-1"
        >
          <span>Open LeetCode</span>
          <ExternalLink className="w-3 h-3" />
        </a>

        {item.status === 'Completed' ? (
          <span className="text-xs text-emerald-400 font-semibold inline-flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Revised
          </span>
        ) : (
          <div className="flex items-center gap-1.5">
            <button
              onClick={onSkip}
              className="px-2.5 py-1 text-xs font-medium text-slate-400 hover:text-slate-200 bg-slate-800 rounded-lg hover:bg-slate-700"
            >
              Skip
            </button>
            <button
              onClick={onComplete}
              className="px-3 py-1 text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-500 rounded-lg shadow-sm"
            >
              Mark Revised
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
