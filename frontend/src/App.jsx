import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Landing } from './pages/Landing';
import { UploadPage } from './pages/UploadPage';
import { PreviewProblems } from './pages/PreviewProblems';
import { ConfigureRoadmap } from './pages/ConfigureRoadmap';
import { RoadmapView } from './pages/RoadmapView';
import { TodayProblems } from './pages/TodayProblems';
import { ProgressDashboard } from './pages/ProgressDashboard';
import { RevisionPage } from './pages/RevisionPage';
import { SettingsPage } from './pages/SettingsPage';
import { AIChatWidget } from './components/AIChatWidget';

export const App = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-brand-500 selection:text-white">
        {/* Top Navbar */}
        <Navbar />

        {/* Main Content Area */}
        <main className="flex-1 pb-16">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/preview" element={<PreviewProblems />} />
            <Route path="/configure" element={<ConfigureRoadmap />} />
            <Route path="/roadmap" element={<RoadmapView />} />
            <Route path="/today" element={<TodayProblems />} />
            <Route path="/progress" element={<ProgressDashboard />} />
            <Route path="/revision" element={<RevisionPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </main>

        {/* Clean Minimal Footer */}
        <footer className="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
            <span>DSA Roadmap AI • Intelligent Prerequisite & Spaced Repetition Engine</span>
            <span>Deterministic Graph Ordering + Concept Interleaving</span>
          </div>
        </footer>

        {/* Global AI Chat Widget — visible on all pages */}
        <AIChatWidget />
      </div>
    </BrowserRouter>
  );
};

export default App;
