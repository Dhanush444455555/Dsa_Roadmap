import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, 
  FileText, 
  FileSpreadsheet, 
  Sparkles, 
  Download, 
  AlertCircle, 
  Loader2, 
  CheckCircle2,
  FileCode,
  Layers,
  ArrowRight
} from 'lucide-react';
import { dsaApi } from '../services/api';
import { useDSAStore } from '../store/useDSAStore';

export const UploadPage = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const { setImportedProblems, setUseBuiltIn } = useDSAStore();

  const [activeTab, setActiveTab] = useState('file'); // 'file' or 'text'
  const [pastedText, setPastedText] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = async (file) => {
    setSelectedFile(file);
    setErrorMsg('');
    setIsLoading(true);

    try {
      const data = await dsaApi.uploadDocument(file);
      if (data && data.problems && data.problems.length > 0) {
        setImportedProblems(data.problems, {
          filename: data.filename,
          fileType: data.file_type,
          count: data.total_problems_detected
        });
        setUseBuiltIn(false);
        navigate('/preview');
      } else {
        setErrorMsg('Could not detect standard LeetCode problems in this document. Please check the format or paste lines directly.');
      }
    } catch (err) {
      console.error(err);
      setErrorMsg(err.response?.data?.detail || 'Failed to upload and parse document. Please check your connection or file format.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  const handleTextParse = async () => {
    if (!pastedText.trim()) {
      setErrorMsg('Please paste some problem titles or numbers.');
      return;
    }

    setErrorMsg('');
    setIsLoading(true);

    try {
      const data = await dsaApi.parseText(pastedText);
      if (data && data.problems && data.problems.length > 0) {
        setImportedProblems(data.problems, {
          filename: 'pasted_text.txt',
          fileType: 'txt',
          count: data.total_problems_detected
        });
        setUseBuiltIn(false);
        navigate('/preview');
      } else {
        setErrorMsg('No recognized LeetCode problems found in pasted text.');
      }
    } catch (err) {
      console.error(err);
      setErrorMsg(err.response?.data?.detail || 'Failed to parse text.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUseBuiltIn = async () => {
    setIsLoading(true);
    try {
      const builtIn = await dsaApi.getBuiltInProblems();
      setImportedProblems(builtIn, {
        filename: 'Curated LeetCode SDE Problem Set',
        fileType: 'built_in',
        count: builtIn.length
      });
      setUseBuiltIn(true);
      navigate('/preview');
    } catch (err) {
      console.error(err);
      setErrorMsg('Failed to load built-in problem dataset.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col gap-8">
      {/* Page Header */}
      <div className="flex flex-col gap-2 text-center sm:text-left">
        <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
          Upload Your DSA Sheet
        </h1>
        <p className="text-sm sm:text-base text-slate-300">
          Upload your LeetCode sheet in PDF, DOCX, TXT, or CSV format. The parser will automatically extract and classify problems.
        </p>
      </div>

      {/* Mode Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('file')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
            activeTab === 'file'
              ? 'bg-brand-600/20 text-brand-400 border border-brand-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
          }`}
        >
          <Upload className="w-4 h-4" />
          File Upload (PDF / DOCX / CSV / TXT)
        </button>

        <button
          onClick={() => setActiveTab('text')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
            activeTab === 'text'
              ? 'bg-brand-600/20 text-brand-400 border border-brand-500/40 shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
          }`}
        >
          <FileText className="w-4 h-4" />
          Direct Text Paste
        </button>
      </div>

      {/* Error Message */}
      {errorMsg && (
        <div className="flex items-start gap-3 bg-rose-500/10 border border-rose-500/30 text-rose-300 p-4 rounded-xl text-sm">
          <AlertCircle className="w-5 h-5 shrink-0 text-rose-400 mt-0.5" />
          <div className="flex flex-col gap-1">
            <span className="font-semibold">Import Issue</span>
            <span>{errorMsg}</span>
          </div>
        </div>
      )}

      {/* Tab 1: File Dropzone */}
      {activeTab === 'file' && (
        <div className="flex flex-col gap-6">
          <div
            onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-2xl p-8 sm:p-14 text-center cursor-pointer transition-all duration-200 flex flex-col items-center justify-center gap-4 ${
              isDragOver
                ? 'border-brand-400 bg-brand-500/10 scale-[0.99]'
                : 'border-slate-700 hover:border-slate-500 bg-slate-900/60 hover:bg-slate-900/90'
            }`}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".pdf,.docx,.doc,.txt,.csv,.tsv"
              className="hidden"
            />

            <div className="p-4 rounded-2xl bg-slate-800 border border-slate-700 text-brand-400 shadow-md">
              {isLoading ? (
                <Loader2 className="w-8 h-8 animate-spin" />
              ) : (
                <Upload className="w-8 h-8" />
              )}
            </div>

            <div className="flex flex-col gap-1">
              <span className="text-base sm:text-lg font-bold text-white">
                {isLoading ? 'Parsing Document & Classifying Problems...' : 'Click to upload or drag & drop your DSA sheet'}
              </span>
              <span className="text-xs text-slate-400">
                Supports PDF, DOCX, TXT, CSV (Max 10MB)
              </span>
            </div>

            {selectedFile && !isLoading && (
              <div className="mt-2 inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-slate-200">
                <FileText className="w-3.5 h-3.5 text-brand-400" />
                <span>{selectedFile.name}</span>
              </div>
            )}
          </div>

          {/* Sample Files Download */}
          <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2.5">
              <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-semibold text-slate-300">
                Need a sample sheet for testing?
              </span>
            </div>

            <div className="flex items-center gap-2 flex-wrap">
              <a
                href="http://localhost:8000/api/sample-files/sample_dsa_sheet.txt"
                download="sample_dsa_sheet.txt"
                className="inline-flex items-center gap-1.5 px-3 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 rounded-lg transition-colors"
              >
                <Download className="w-3 h-3 text-slate-400" />
                Sample .TXT
              </a>

              <a
                href="http://localhost:8000/api/sample-files/sample_dsa_sheet.csv"
                download="sample_dsa_sheet.csv"
                className="inline-flex items-center gap-1.5 px-3 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 rounded-lg transition-colors"
              >
                <Download className="w-3 h-3 text-slate-400" />
                Sample .CSV
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Text Paste */}
      {activeTab === 'text' && (
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-2">
            <label className="text-xs font-semibold text-slate-300">
              Paste problem list or messy text:
            </label>
            <textarea
              value={pastedText}
              onChange={(e) => setPastedText(e.target.value)}
              placeholder={`55 — Jump Game\n121 — Best Time to Buy and Sell Stock\n141 — Linked List Cycle\n206 — Reverse Linked List\n704 — Binary Search\n875 — Koko Eating Bananas\n1046 — Last Stone Weight\n1710 — Maximum Units on a Truck\n1834 — Single-Threaded CPU`}
              rows={9}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-sm text-slate-100 font-mono placeholder-slate-600 focus:outline-none focus:border-brand-500 transition-colors"
            />
          </div>

          <button
            onClick={handleTextParse}
            disabled={isLoading}
            className="inline-flex items-center justify-center gap-2 bg-brand-600 hover:bg-brand-500 disabled:bg-slate-800 text-white font-semibold px-6 py-3 rounded-xl shadow-md transition-all"
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
            <span>Parse and Extract Problems</span>
          </button>
        </div>
      )}

      {/* Built-in Fallback Action (Section 23 requirement) */}
      <div className="border-t border-slate-800/80 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <span className="text-sm font-bold text-white block">
              Don't have a personal DSA sheet?
            </span>
            <span className="text-xs text-slate-400">
              Start immediately with our curated Top SDE Sheet (150+ categorized problems).
            </span>
          </div>
        </div>

        <button
          onClick={handleUseBuiltIn}
          disabled={isLoading}
          className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-600 text-white font-semibold text-xs px-4 py-2.5 rounded-xl transition-all shadow-sm"
        >
          <span>Use Built-in Problem Set</span>
          <ArrowRight className="w-3.5 h-3.5 text-brand-400" />
        </button>
      </div>
    </div>
  );
};
