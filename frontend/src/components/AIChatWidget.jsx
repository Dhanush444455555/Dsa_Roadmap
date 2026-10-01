import React, { useState, useRef, useEffect } from 'react';
import {
  MessageCircle,
  X,
  Send,
  Loader2,
  Bot,
  User,
  Sparkles,
  RotateCcw,
  ChevronDown,
  Lightbulb,
} from 'lucide-react';
import { dsaApi } from '../services/api';

// Simple markdown-like renderer for AI responses
const MessageContent = ({ text }) => {
  if (!text) return null;

  const parts = text.split(/(```[\s\S]*?```)/g);

  return (
    <div className="text-sm leading-relaxed space-y-2">
      {parts.map((part, i) => {
        if (part.startsWith('```')) {
          const codeContent = part.replace(/^```\w*\n?/, '').replace(/```$/, '');
          return (
            <pre key={i} className="bg-slate-950 border border-slate-700 rounded-lg p-3 text-xs font-mono text-emerald-300 overflow-x-auto whitespace-pre-wrap">
              {codeContent}
            </pre>
          );
        }
        // Process inline formatting
        const lines = part.split('\n');
        return (
          <div key={i}>
            {lines.map((line, j) => {
              if (!line.trim()) return <br key={j} />;
              // Bold
              const formatted = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
              // Bullet points
              if (line.trim().startsWith('- ') || line.trim().startsWith('• ')) {
                return (
                  <div key={j} className="flex gap-2 ml-2">
                    <span className="text-brand-400 shrink-0">•</span>
                    <span dangerouslySetInnerHTML={{ __html: formatted.replace(/^[-•]\s*/, '') }} />
                  </div>
                );
              }
              // Blockquotes (tips)
              if (line.trim().startsWith('>')) {
                return (
                  <div key={j} className="border-l-2 border-indigo-500 pl-3 py-0.5 bg-indigo-950/30 rounded-r text-xs text-indigo-300 italic">
                    <span dangerouslySetInnerHTML={{ __html: formatted.replace(/^>\s*/, '') }} />
                  </div>
                );
              }
              // Numbered list
              if (/^\d+\./.test(line.trim())) {
                return (
                  <div key={j} className="flex gap-2 ml-2">
                    <span className="text-brand-400 shrink-0 font-mono text-xs">{line.match(/^\d+/)[0]}.</span>
                    <span dangerouslySetInnerHTML={{ __html: formatted.replace(/^\d+\.\s*/, '') }} />
                  </div>
                );
              }
              // Headings (##)
              if (line.startsWith('## ') || line.startsWith('# ')) {
                return (
                  <p key={j} className="font-bold text-white mt-1" dangerouslySetInnerHTML={{ __html: formatted.replace(/^#{1,3}\s*/, '') }} />
                );
              }
              return (
                <p key={j} dangerouslySetInnerHTML={{ __html: formatted }} />
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

const QUICK_PROMPTS = [
  { label: '💡 Give a hint', message: 'Give me a hint for this problem without revealing the full solution.' },
  { label: '⏱️ Time complexity', message: 'What is the time and space complexity of the optimal approach?' },
  { label: '🔍 Explain pattern', message: 'What algorithmic pattern should I use here and why?' },
  { label: '📝 Walk me through', message: 'Walk me through the optimal approach step by step.' },
];

export const AIChatWidget = ({ problemContext = null }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'model',
      content: "👋 Hi! I'm **AlgoBot**, your DSA tutor powered by Google Gemini AI!\n\nAsk me anything about:\n- 💡 Problem hints & approaches\n- ⏱️ Time/Space complexity\n- 📚 DSA patterns & templates\n- 🎯 Interview tips",
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [unread, setUnread] = useState(0);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
      setUnread(0);
    }
  }, [messages, isOpen]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const sendMessage = async (text = input.trim()) => {
    if (!text || isLoading) return;

    const userMsg = { role: 'user', content: text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    // Build history for API (exclude greeting)
    const history = newMessages.slice(1, -1).map((m) => ({
      role: m.role,
      content: m.content,
    }));

    try {
      const result = await dsaApi.aiChat(text, history, problemContext);
      const botMsg = {
        role: 'model',
        content: result.reply,
        model: result.model_used,
      };
      setMessages((prev) => [...prev, botMsg]);
      if (!isOpen) setUnread((n) => n + 1);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'model',
          content: '⚠️ Oops! I had trouble connecting. Please try again.',
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleReset = () => {
    setMessages([
      {
        role: 'model',
        content: "Chat cleared! I'm ready to help again. What would you like to know?",
      },
    ]);
  };

  return (
    <>
      {/* Floating Bubble Button */}
      <button
        onClick={() => { setIsOpen((o) => !o); setIsMinimized(false); }}
        className={`fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full flex items-center justify-center shadow-2xl transition-all duration-300 hover:scale-110 ${
          isOpen
            ? 'bg-slate-800 border border-slate-600'
            : 'bg-gradient-to-br from-brand-600 to-purple-600 hover:from-brand-500 hover:to-purple-500'
        }`}
        aria-label="Open AI Chat"
      >
        {isOpen ? (
          <X className="w-6 h-6 text-white" />
        ) : (
          <>
            <Bot className="w-6 h-6 text-white" />
            {unread > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center justify-center">
                {unread}
              </span>
            )}
          </>
        )}
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div
          className={`fixed bottom-24 right-6 z-50 w-[380px] max-w-[calc(100vw-3rem)] flex flex-col rounded-2xl shadow-2xl border border-slate-700/80 bg-slate-900 transition-all duration-300 ${
            isMinimized ? 'h-14' : 'h-[520px]'
          }`}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-gradient-to-r from-slate-900 to-indigo-950/50 rounded-t-2xl shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="relative">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-400 border-2 border-slate-900" />
              </div>
              <div>
                <p className="text-sm font-bold text-white">AlgoBot</p>
                <p className="text-[10px] text-emerald-400 flex items-center gap-1">
                  <Sparkles className="w-2.5 h-2.5" />
                  Powered by Gemini AI
                </p>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button
                onClick={handleReset}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                title="Clear chat"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setIsMinimized((m) => !m)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                title={isMinimized ? 'Expand' : 'Minimize'}
              >
                <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isMinimized ? 'rotate-180' : ''}`} />
              </button>
            </div>
          </div>

          {/* Problem Context Banner */}
          {!isMinimized && problemContext && (
            <div className="px-3 py-2 bg-indigo-950/40 border-b border-indigo-500/20 flex items-center gap-2 shrink-0">
              <Lightbulb className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
              <span className="text-[11px] text-indigo-300 truncate">
                Context: #{problemContext.number} {problemContext.title}
              </span>
            </div>
          )}

          {/* Messages */}
          {!isMinimized && (
            <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3 scrollbar-thin scrollbar-thumb-slate-700">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex gap-2.5 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  {/* Avatar */}
                  <div className={`w-7 h-7 rounded-full shrink-0 flex items-center justify-center ${
                    msg.role === 'user'
                      ? 'bg-brand-600'
                      : 'bg-gradient-to-br from-indigo-600 to-purple-700'
                  }`}>
                    {msg.role === 'user'
                      ? <User className="w-3.5 h-3.5 text-white" />
                      : <Bot className="w-3.5 h-3.5 text-white" />
                    }
                  </div>

                  {/* Bubble */}
                  <div className={`max-w-[78%] rounded-2xl px-3 py-2.5 ${
                    msg.role === 'user'
                      ? 'bg-brand-600 text-white rounded-tr-sm'
                      : msg.isError
                      ? 'bg-red-950/40 border border-red-500/30 text-red-300 rounded-tl-sm'
                      : 'bg-slate-800 text-slate-100 rounded-tl-sm'
                  }`}>
                    {msg.role === 'user' ? (
                      <p className="text-sm">{msg.content}</p>
                    ) : (
                      <MessageContent text={msg.content} />
                    )}
                    {msg.model && msg.model !== 'rule-based-fallback' && (
                      <p className="text-[10px] text-slate-500 mt-1.5 text-right">via {msg.model}</p>
                    )}
                  </div>
                </div>
              ))}

              {/* Loading indicator */}
              {isLoading && (
                <div className="flex gap-2.5">
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-600 to-purple-700 flex items-center justify-center shrink-0">
                    <Bot className="w-3.5 h-3.5 text-white" />
                  </div>
                  <div className="bg-slate-800 rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-1.5">
                    {[0, 1, 2].map((n) => (
                      <span
                        key={n}
                        className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce"
                        style={{ animationDelay: `${n * 0.15}s` }}
                      />
                    ))}
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          )}

          {/* Quick Prompts */}
          {!isMinimized && messages.length <= 2 && !isLoading && (
            <div className="px-3 pb-2 flex flex-wrap gap-1.5 shrink-0">
              {QUICK_PROMPTS.map((p) => (
                <button
                  key={p.label}
                  onClick={() => sendMessage(p.message)}
                  className="text-[11px] px-2.5 py-1 rounded-full bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 hover:text-white transition-colors"
                >
                  {p.label}
                </button>
              ))}
            </div>
          )}

          {/* Input */}
          {!isMinimized && (
            <div className="px-3 pb-3 shrink-0">
              <div className="flex items-end gap-2 bg-slate-800 border border-slate-700 rounded-xl p-2 focus-within:border-brand-500 transition-colors">
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask anything DSA..."
                  rows={1}
                  className="flex-1 bg-transparent text-sm text-slate-100 placeholder-slate-500 resize-none focus:outline-none max-h-24 overflow-y-auto"
                  style={{ minHeight: '24px' }}
                />
                <button
                  onClick={() => sendMessage()}
                  disabled={!input.trim() || isLoading}
                  className="w-8 h-8 rounded-lg bg-brand-600 hover:bg-brand-500 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center shrink-0 transition-colors"
                >
                  {isLoading ? (
                    <Loader2 className="w-3.5 h-3.5 text-white animate-spin" />
                  ) : (
                    <Send className="w-3.5 h-3.5 text-white" />
                  )}
                </button>
              </div>
              <p className="text-[10px] text-slate-600 text-center mt-1.5">
                Press Enter to send • Shift+Enter for new line
              </p>
            </div>
          )}
        </div>
      )}
    </>
  );
};

export default AIChatWidget;
