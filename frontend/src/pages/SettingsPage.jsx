import React, { useState } from 'react';
import { 
  Settings, 
  Key, 
  Database, 
  RefreshCw, 
  Download, 
  Upload, 
  CheckCircle2, 
  AlertTriangle,
  FileText
} from 'lucide-react';
import { useDSAStore } from '../store/useDSAStore';
import { dsaApi } from '../services/api';

export const SettingsPage = () => {
  const { activeRoadmap, setActiveRoadmap, setImportedProblems } = useDSAStore();
  const [apiKey, setApiKey] = useState('');
  const [saveStatus, setSaveStatus] = useState('');

  const handleSaveApiKey = () => {
    if (!apiKey.trim()) return;
    localStorage.setItem('dsa_llm_api_key', apiKey);
    setSaveStatus('API Key saved to browser local storage.');
    setTimeout(() => setSaveStatus(''), 3000);
  };

  const handleResetToBuiltIn = async () => {
    try {
      const data = await dsaApi.getBuiltInProblems();
      setImportedProblems(data, {
        filename: 'Curated LeetCode SDE Problem Set',
        fileType: 'built_in',
        count: data.length
      });
      setSaveStatus('Reset to built-in problem set successfully!');
      setTimeout(() => setSaveStatus(''), 3000);
    } catch (err) {
      console.error(err);
    }
  };

  const handleExportJSON = () => {
    if (!activeRoadmap) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(activeRoadmap, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `DSA_Roadmap_Backup.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col gap-8">
      {/* Header */}
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
          Application Settings
        </h1>
        <p className="text-sm sm:text-base text-slate-300">
          Configure API keys, manage offline problem datasets, and backup your preparation progress.
        </p>
      </div>

      {saveStatus && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-sm flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{saveStatus}</span>
        </div>
      )}

      {/* LLM API Configuration (Section 24 & 26 Security) */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col gap-4 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
            <Key className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white">
              AI / LLM API Key (Optional)
            </h2>
            <p className="text-xs text-slate-400">
              For extracting concepts from messy documents. By default, the system uses deterministic rules & our curated dataset.
            </p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-3 pt-2">
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter Gemini / OpenAI API Key..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:border-brand-500"
          />
          <button
            onClick={handleSaveApiKey}
            className="w-full sm:w-auto px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs rounded-xl shadow-sm transition-all shrink-0"
          >
            Save Key
          </button>
        </div>
      </div>

      {/* Dataset Management */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col gap-4 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white">
              Curated Problem Dataset & Samples
            </h2>
            <p className="text-xs text-slate-400">
              Reset imported state or download test sheets in different formats.
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3 pt-2">
          <button
            onClick={handleResetToBuiltIn}
            className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 rounded-xl transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5 text-brand-400" />
            Reload Built-in SDE Sheet (150+ Problems)
          </button>

          <a
            href="http://localhost:8000/api/sample-files/sample_dsa_sheet.txt"
            download="sample_dsa_sheet.txt"
            className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 rounded-xl transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-slate-400" />
            Download Sample .TXT
          </a>

          <a
            href="http://localhost:8000/api/sample-files/sample_dsa_sheet.csv"
            download="sample_dsa_sheet.csv"
            className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 rounded-xl transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-slate-400" />
            Download Sample .CSV
          </a>
        </div>
      </div>

      {/* Backup and Export */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-sm">
        <div>
          <h3 className="text-sm font-bold text-white">
            Export Active Roadmap Backup
          </h3>
          <p className="text-xs text-slate-400">
            Download your active roadmap hierarchy and completion status in JSON format.
          </p>
        </div>

        <button
          onClick={handleExportJSON}
          className="inline-flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs rounded-xl shadow-sm transition-all shrink-0"
        >
          <Download className="w-4 h-4" />
          Export JSON
        </button>
      </div>
    </div>
  );
};
