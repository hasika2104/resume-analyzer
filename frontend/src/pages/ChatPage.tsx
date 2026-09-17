import { useEffect, useState, useRef } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';
import toast from 'react-hot-toast';
import { chatApi, analysisApi } from '../services/api';
import type { ChatMessage, ResumeHistoryItem } from '../types';

const SUGGESTIONS = [
  'What is wrong with my resume?',
  'How can I improve my ATS score?',
  'Which jobs am I eligible for?',
  'Which skills should I learn next?',
  'Rewrite my project descriptions',
  'Generate interview questions from my resume',
  'Suggest certifications for my target role',
  'Generate a professional summary',
];

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<ResumeHistoryItem[]>([]);
  const [selectedResume, setSelectedResume] = useState<number | ''>('');
  const [gptEnabled, setGptEnabled] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatApi.history().then(setMessages);
    analysisApi.history().then(setHistory);
    chatApi.status().then((s) => setGptEnabled(s.openai_enabled));
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const send = async (text?: string) => {
    const msg = (text || input).trim();
    if (!msg) return;
    setInput('');
    setLoading(true);
    setMessages((prev) => [...prev, { id: Date.now(), role: 'user', content: msg, created_at: new Date().toISOString() }]);

    try {
      const response = await chatApi.send(msg, selectedResume ? Number(selectedResume) : undefined);
      setMessages((prev) => [...prev, response]);
    } catch {
      toast.error('Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] animate-fade-in-up">
      <div className="mb-4">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-bold">OpenAI Career Copilot</h1>
          {gptEnabled ? (
            <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full flex items-center gap-1">
              <Sparkles size={12} /> GPT Active
            </span>
          ) : (
            <span className="px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full">Rule-based mode — set OPENAI_API_KEY</span>
          )}
        </div>
        <p className="text-slate-500 mt-1">RAG-powered assistant with your resume context</p>
        {history.length > 0 && (
          <select className="input w-auto mt-3 text-sm" value={selectedResume} onChange={(e) => setSelectedResume(e.target.value ? Number(e.target.value) : '')}>
            <option value="">General chat</option>
            {history.map((h) => (
              <option key={h.id} value={h.id}>{h.file_name} (ATS: {h.ats_score})</option>
            ))}
          </select>
        )}
      </div>

      <div className="card flex-1 flex flex-col overflow-hidden !p-0">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-8">
              <Bot className="mx-auto text-indigo-400 mb-4" size={48} />
              <p className="text-slate-500 mb-4">Ask anything about your career journey</p>
              <div className="flex flex-wrap gap-2 justify-center max-w-2xl mx-auto">
                {SUGGESTIONS.map((s) => (
                  <button key={s} onClick={() => send(s)} className="px-3 py-1.5 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 text-xs rounded-full hover:bg-indigo-100 transition">
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}
          {messages.map((msg) => (
            <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shrink-0">
                  <Bot size={16} className="text-white" />
                </div>
              )}
              <div className={`max-w-[80%] p-3 rounded-2xl text-sm whitespace-pre-wrap ${
                msg.role === 'user' ? 'bg-indigo-600 text-white rounded-br-md' : 'bg-slate-100 dark:bg-slate-800 rounded-bl-md'
              }`}>
                {msg.content}
              </div>
              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center shrink-0">
                  <User size={16} />
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="flex gap-2 items-center text-sm text-slate-500">
              <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
              <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="p-4 border-t border-slate-200 dark:border-slate-800">
          <div className="flex gap-2">
            <input
              className="input"
              placeholder="Ask about resume, skills, interviews, salary..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !loading && send()}
            />
            <button onClick={() => send()} disabled={loading || !input.trim()} className="btn-primary !px-4">
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
