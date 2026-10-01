import React, { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  Compass, 
  Upload, 
  Map, 
  CheckCircle2, 
  BarChart3, 
  RotateCcw, 
  Settings, 
  Flame,
  Sparkles,
  User as UserIcon,
  LogOut,
  LogIn
} from 'lucide-react';
import { dsaApi } from '../services/api';
import { useAuthStore } from '../store/useAuthStore';

export const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuthStore();
  const [streak, setStreak] = useState(1);
  const [completedCount, setCompletedCount] = useState(0);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    dsaApi.getProgress()
      .then((res) => {
        if (res) {
          setStreak(res.current_streak || 1);
          setCompletedCount(res.completed || 0);
        }
      })
      .catch(() => {});
  }, [location.pathname]);

  const navLinks = [
    { name: 'Upload Sheet', path: '/upload', icon: Upload },
    { name: 'Roadmap', path: '/roadmap', icon: Map },
    { name: 'Today', path: '/today', icon: CheckCircle2 },
    { name: 'Progress', path: '/progress', icon: BarChart3 },
    { name: 'Revision', path: '/revision', icon: RotateCcw },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-brand-500/25 group-hover:scale-105 transition-transform duration-200">
              <Compass className="w-6 h-6 text-white animate-spin-slow" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                DSA Roadmap <span className="text-brand-400">AI</span>
              </span>
              <span className="hidden sm:block text-[10px] uppercase font-semibold tracking-wider text-slate-400">
                Personalized Preparation Engine
              </span>
            </div>
          </Link>

          {/* Nav Items */}
          <nav className="hidden md:flex items-center gap-1 lg:gap-2">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.path;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-brand-500/15 text-brand-400 border border-brand-500/30 shadow-sm'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-brand-400' : 'text-slate-400'}`} />
                  {link.name}
                </Link>
              );
            })}
          </nav>

          {/* Quick Stats & User Profile Pill */}
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="flex items-center gap-1.5 sm:gap-2 bg-slate-800/80 border border-slate-700/60 px-2.5 sm:px-3 py-1.5 rounded-full text-xs font-semibold text-amber-300 shadow-inner">
              <Flame className="w-4 h-4 text-amber-400 animate-pulse" />
              <span>{streak}d Streak</span>
            </div>

            {/* Auth Button or User Menu */}
            {isAuthenticated && user ? (
              <div className="relative">
                <button
                  onClick={() => setMenuOpen(!menuOpen)}
                  className="flex items-center gap-2 bg-slate-800 hover:bg-slate-750 border border-slate-700 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-200 transition-colors"
                >
                  <div className="w-5 h-5 rounded-full bg-brand-600 flex items-center justify-center text-[10px] text-white font-bold">
                    {(user.name || user.email || 'U').charAt(0).toUpperCase()}
                  </div>
                  <span className="max-w-[80px] sm:max-w-[120px] truncate">{user.name || user.email.split('@')[0]}</span>
                </button>

                {menuOpen && (
                  <div 
                    className="absolute right-0 mt-2 w-48 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl py-1 z-50 animate-in fade-in slide-in-from-top-2"
                    onMouseLeave={() => setMenuOpen(false)}
                  >
                    <div className="px-3 py-2 border-b border-slate-800">
                      <p className="text-xs font-bold text-white truncate">{user.name || 'Learner'}</p>
                      <p className="text-[11px] text-slate-400 truncate">{user.email}</p>
                    </div>
                    <Link
                      to="/settings"
                      onClick={() => setMenuOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
                    >
                      <Settings className="w-3.5 h-3.5 text-slate-400" />
                      Settings & Preferences
                    </Link>
                    <button
                      onClick={() => {
                        setMenuOpen(false);
                        logout();
                        navigate('/');
                      }}
                      className="w-full flex items-center gap-2 px-3 py-2 text-xs text-red-400 hover:bg-red-950/40 transition-colors text-left"
                    >
                      <LogOut className="w-3.5 h-3.5" />
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link
                to="/login"
                className="inline-flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 hover:border-slate-600 text-xs font-semibold px-3 py-1.5 rounded-lg shadow-sm transition-all"
              >
                <LogIn className="w-3.5 h-3.5 text-brand-400" />
                <span>Sign In</span>
              </Link>
            )}

            <Link
              to="/configure"
              className="hidden sm:inline-flex items-center gap-1.5 bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white text-xs font-semibold px-3.5 py-2 rounded-lg shadow-md shadow-brand-600/20 transition-all hover:scale-[1.02]"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>New</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Mobile nav bar at bottom of header */}
      <div className="md:hidden flex items-center justify-around py-2 border-t border-slate-800/60 bg-slate-900/95 overflow-x-auto">
        {navLinks.map((link) => {
          const Icon = link.icon;
          const isActive = location.pathname === link.path;
          return (
            <Link
              key={link.path}
              to={link.path}
              className={`flex flex-col items-center gap-1 px-2.5 py-1 text-[11px] font-medium ${
                isActive ? 'text-brand-400' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4" />
              {link.name}
            </Link>
          );
        })}
      </div>
    </header>
  );
};
