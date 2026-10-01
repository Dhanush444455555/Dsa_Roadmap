import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Mail, User, Calendar, ArrowRight, Loader2,
  CheckCircle2, Sparkles, AlertCircle, ShieldCheck, Compass
} from 'lucide-react';
import { useAuthStore } from '../store/useAuthStore';

// ─────────────────────────────────────────────
// Animated DSA background canvas
// ─────────────────────────────────────────────
const DSA_TOKENS = [
  'O(n log n)', 'O(1)', 'BFS', 'DFS', 'dp[i][j]',
  'left++', 'right--', 'mid = (lo+hi)>>1', 'stack.push()',
  'while(lo<=hi)', 'queue.poll()', 'graph[u].push(v)',
  'memo[n]', 'two-pointer', 'sliding window', '// O(n)',
  'heap.offer()', 'union(x,y)', 'return dp[n]', 'trie.insert()',
  'preSum[i]', 'visited.add(node)', '#include', 'def solve():',
  'import java.util.*', 'max(dp)', 'Arrays.sort(arr)',
];

const AnimatedBackground = () => {
  const canvasRef = useRef(null);
  const particlesRef = useRef([]);
  const rafRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    // Initialize particles
    const COUNT = 28;
    particlesRef.current = Array.from({ length: COUNT }, (_, i) => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      text: DSA_TOKENS[i % DSA_TOKENS.length],
      opacity: 0.04 + Math.random() * 0.1,
      size: 10 + Math.random() * 8,
      color: ['#818cf8', '#a78bfa', '#38bdf8', '#34d399', '#f472b6'][Math.floor(Math.random() * 5)],
    }));

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particlesRef.current.forEach((p) => {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < -200) p.x = canvas.width + 100;
        if (p.x > canvas.width + 200) p.x = -100;
        if (p.y < -50) p.y = canvas.height + 50;
        if (p.y > canvas.height + 50) p.y = -50;

        ctx.save();
        ctx.globalAlpha = p.opacity;
        ctx.fillStyle = p.color;
        ctx.font = `${p.size}px 'JetBrains Mono', 'Fira Code', monospace`;
        ctx.fillText(p.text, p.x, p.y);
        ctx.restore();
      });
      rafRef.current = requestAnimationFrame(draw);
    };
    draw();

    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(rafRef.current);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 z-0 pointer-events-none"
    />
  );
};

// ─────────────────────────────────────────────
// Input Field Component
// ─────────────────────────────────────────────
const InputField = ({ id, type = 'text', label, placeholder, value, onChange, icon: Icon, rightElement, error, hint }) => (
  <div className="flex flex-col gap-1.5">
    <div className="flex items-center justify-between">
      <label htmlFor={id} className="text-xs font-semibold text-slate-300 tracking-wide">
        {label}
      </label>
      {hint && <span className="text-[11px] text-slate-500">{hint}</span>}
    </div>
    <div className={`relative flex items-center bg-slate-950/70 border rounded-xl transition-all focus-within:ring-1 ${
      error
        ? 'border-red-500/60 focus-within:ring-red-500/30'
        : 'border-slate-700/60 focus-within:border-brand-500/80 focus-within:ring-brand-500/20'
    }`}>
      {Icon && (
        <div className="pl-3.5 shrink-0 text-slate-500">
          <Icon className="w-4 h-4" />
        </div>
      )}
      <input
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        autoComplete={id}
        className="flex-1 bg-transparent px-3 py-3 text-sm text-slate-100 placeholder-slate-600 focus:outline-none [color-scheme:dark]"
      />
      {rightElement && <div className="pr-3 shrink-0">{rightElement}</div>}
    </div>
    {error && (
      <p className="text-xs text-red-400 flex items-center gap-1 mt-0.5">
        <AlertCircle className="w-3.5 h-3.5 shrink-0" /> {error}
      </p>
    )}
  </div>
);

// ─────────────────────────────────────────────
// Main Login Page
// ─────────────────────────────────────────────
export const LoginPage = () => {
  const navigate = useNavigate();
  const { login, isLoading, error, clearError, isAuthenticated } = useAuthStore();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [fieldErrors, setFieldErrors] = useState({});

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const validate = () => {
    const errors = {};
    if (!name.trim()) {
      errors.name = 'Please enter your full name';
    }
    if (!email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = 'Please enter a valid email address';
    }
    if (!dateOfBirth) {
      errors.dateOfBirth = 'Please select your date of birth';
    } else {
      const selectedDate = new Date(dateOfBirth);
      const now = new Date();
      if (selectedDate > now) {
        errors.dateOfBirth = 'Date of birth cannot be in the future';
      }
    }
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    clearError();
    if (!validate()) return;

    const result = await login({
      name,
      email,
      date_of_birth: dateOfBirth,
      rememberMe,
    });

    if (result.success) {
      navigate('/roadmap', { replace: true });
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated canvas background */}
      <AnimatedBackground />

      {/* Gradient blobs */}
      <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-brand-600/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-1/3 -right-32 w-80 h-80 bg-purple-600/8 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1.5s' }} />
        <div className="absolute -bottom-40 left-1/3 w-80 h-80 bg-indigo-600/8 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '3s' }} />
      </div>

      {/* Card */}
      <div className="relative z-10 w-full max-w-md">
        {/* Logo / Brand */}
        <div className="text-center mb-6">
          <Link to="/" className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-bold tracking-wider mb-4 hover:bg-brand-500/15 transition-all">
            <Compass className="w-4 h-4 text-brand-400 animate-spin-slow" />
            DSA Roadmap AI
          </Link>
          <h1 className="text-3xl font-black text-white tracking-tight">
            Welcome to Pathfinder
          </h1>
          <p className="text-sm text-slate-400 mt-2">
            Sign in or auto-register using your profile details
          </p>
        </div>

        {/* Glassmorphism Card */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 sm:p-8 shadow-2xl shadow-black/40">
          
          {/* Info Banner */}
          <div className="flex items-start gap-3 p-3.5 rounded-xl bg-brand-950/40 border border-brand-500/20 text-brand-300 text-xs mb-6">
            <ShieldCheck className="w-5 h-5 text-brand-400 shrink-0 mt-0.5" />
            <span className="leading-relaxed">
              Authenticate securely with your <strong>Full Name</strong>, <strong>Email</strong>, and <strong>Date of Birth</strong>.
            </span>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4" noValidate>
            {/* Global Error */}
            {error && (
              <div className="flex items-start gap-2.5 p-3.5 rounded-xl bg-red-950/40 border border-red-500/30 text-red-300 text-xs">
                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            {/* Name field */}
            <InputField
              id="name"
              label="Full Name"
              placeholder="e.g. Dhanush D"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                if (fieldErrors.name) setFieldErrors(prev => ({ ...prev, name: null }));
              }}
              icon={User}
              error={fieldErrors.name}
            />

            {/* Email */}
            <InputField
              id="email"
              type="email"
              label="Email Address"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (fieldErrors.email) setFieldErrors(prev => ({ ...prev, email: null }));
              }}
              icon={Mail}
              error={fieldErrors.email}
            />

            {/* Date of Birth */}
            <InputField
              id="dob"
              type="date"
              label="Date of Birth"
              placeholder="YYYY-MM-DD"
              value={dateOfBirth}
              onChange={(e) => {
                setDateOfBirth(e.target.value);
                if (fieldErrors.dateOfBirth) setFieldErrors(prev => ({ ...prev, dateOfBirth: null }));
              }}
              icon={Calendar}
              error={fieldErrors.dateOfBirth}
              hint="Required for verification"
            />

            {/* Remember me */}
            <div className="flex items-center justify-between pt-1">
              <label className="flex items-center gap-2 cursor-pointer group select-none">
                <div
                  onClick={() => setRememberMe((v) => !v)}
                  className={`w-4 h-4 rounded border-2 flex items-center justify-center transition-all cursor-pointer ${
                    rememberMe
                      ? 'bg-brand-600 border-brand-600'
                      : 'border-slate-600 group-hover:border-slate-400'
                  }`}
                >
                  {rememberMe && <CheckCircle2 className="w-3 h-3 text-white" />}
                </div>
                <span className="text-xs text-slate-400 group-hover:text-slate-300 transition-colors">
                  Keep me signed in
                </span>
              </label>

              <div className="flex items-center gap-1 text-[11px] text-slate-500">
                <Sparkles className="w-3 h-3 text-amber-400" />
                <span>Auto creates account</span>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              id="auth-submit-btn"
              disabled={isLoading}
              className="mt-3 w-full inline-flex items-center justify-center gap-2 bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed text-white font-bold py-3.5 rounded-xl shadow-lg shadow-brand-600/25 hover:shadow-brand-600/40 hover:scale-[1.01] active:scale-[0.99] transition-all duration-200"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  <span>Continue to Dashboard</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Back link */}
        <div className="text-center mt-5">
          <Link
            to="/"
            className="text-xs text-slate-500 hover:text-slate-300 transition-colors"
          >
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
