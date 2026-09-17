import { useState } from 'react';
import type { AnalysisResult } from '../types';
import ATSScoreRing from './ATSScoreRing';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell,
} from 'recharts';
import {
  Download, Lightbulb, Target, BookOpen, Briefcase, Brain,
  Layout, CheckCircle, AlertTriangle, Sparkles,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { analysisApi } from '../services/api';

interface Props {
  analysis: AnalysisResult;
}

const COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981'];

export default function AnalysisDashboard({ analysis }: Props) {
  const [qaQuestion, setQaQuestion] = useState('');
  const [qaAnswer, setQaAnswer] = useState('');
  const [coverLetter, setCoverLetter] = useState('');

  const breakdownData = Object.entries(analysis.ats_breakdown).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    score: value,
  }));

  const handleDownloadReport = async () => {
    const blob = await analysisApi.downloadPdf(analysis.id);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analysis_${analysis.id}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Report downloaded');
  };

  const handleQA = async () => {
    if (!qaQuestion.trim()) return;
    const data = await analysisApi.qa(analysis.id, qaQuestion);
    setQaAnswer(data.answer);
  };

  const handleCoverLetter = async () => {
    const data = await analysisApi.coverLetter(analysis.id);
    setCoverLetter(data.cover_letter);
    toast.success('Cover letter generated');
  };

  const handleDownloadCoverLetter = async () => {
    if (!coverLetter) {
      toast.error('Generate cover letter first');
      return;
    }
    try {
      const blob = await analysisApi.downloadCoverLetter(analysis.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cover_letter_${analysis.id}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success('Cover letter downloaded');
    } catch (error) {
      toast.error('Failed to download cover letter');
    }
  };

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl font-bold">Resume Analysis</h1>
            {analysis.openai_enabled && (
              <span className="px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 text-xs rounded-full flex items-center gap-1">
                <Sparkles size={12} /> GPT Powered
              </span>
            )}
          </div>
          <p className="text-slate-500">{analysis.file_name}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button onClick={handleDownloadReport} className="btn-secondary flex items-center gap-2 text-sm">
            <Download size={16} /> Analysis PDF
          </button>
        </div>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'ATS Score', value: analysis.ats_score, suffix: '/100', ring: true },
          { label: 'Resume Health', value: analysis.resume_health_score, suffix: '/100' },
          { label: 'Career Readiness', value: analysis.career_readiness_score, suffix: '/100' },
          { label: 'Job Match', value: analysis.job_match_percentage, suffix: '%' },
        ].map(({ label, value, suffix, ring }) => (
          <div key={label} className="card flex flex-col items-center justify-center !p-4">
            {ring ? (
              <ATSScoreRing score={value} size={100} />
            ) : (
              <p className="text-3xl font-bold text-indigo-600">{Math.round(value)}{suffix.replace('/100', '')}</p>
            )}
            <p className="text-xs text-slate-500 mt-2 font-medium">{label}</p>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="card">
        <h2 className="font-semibold flex items-center gap-2 mb-3">
          <Brain size={20} className="text-indigo-500" /> AI Summary
        </h2>
        <p className="text-slate-600 dark:text-slate-300 leading-relaxed">{analysis.ai_summary}</p>
      </div>

      {/* ATS Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-4">ATS Score Breakdown</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={breakdownData}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="score" fill="#6366f1" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h2 className="font-semibold mb-4">Industry Benchmark</h2>
          <div className="space-y-4">
            {[
              ['Your ATS', analysis.analytics.industry_benchmark.your_ats, analysis.analytics.industry_benchmark.industry_avg_ats],
              ['Resume Health', analysis.analytics.industry_benchmark.your_health, analysis.analytics.industry_benchmark.industry_avg_health],
              ['Career Readiness', analysis.analytics.industry_benchmark.your_readiness, analysis.analytics.industry_benchmark.industry_avg_readiness],
            ].map(([label, yours, avg]) => (
              <div key={label as string}>
                <div className="flex justify-between text-sm mb-1">
                  <span>{label as string}</span>
                  <span className="font-semibold">{yours as number} <span className="text-slate-400 font-normal">vs avg {avg as number}</span></span>
                </div>
                <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${yours as number}%` }} />
                </div>
              </div>
            ))}
            <p className="text-sm text-indigo-600 font-medium">
              Top {analysis.analytics.industry_benchmark.percentile}% percentile
            </p>
          </div>
        </div>
      </div>

      {/* Template Evaluation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold flex items-center gap-2 mb-4">
            <Layout size={20} className="text-orange-500" /> Template Evaluation
          </h2>
          <div className="flex items-center gap-4 mb-4">
            <div className="text-4xl font-bold text-orange-600">{analysis.template_evaluation.rating}/10</div>
            <div>
              <p className="text-sm font-medium">{analysis.template_evaluation.ats_friendly ? 'ATS Friendly' : 'Needs Improvement'}</p>
              <p className="text-xs text-slate-500">Readability: {analysis.template_evaluation.readability_score}/100</p>
            </div>
          </div>
          <ul className="space-y-2">
            {analysis.template_evaluation.problems.map((p, i) => (
              <li key={i} className="flex items-start gap-2 text-sm">
                <AlertTriangle size={14} className="text-orange-500 mt-0.5 shrink-0" />
                {p}
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h2 className="font-semibold flex items-center gap-2 mb-4">
            <Layout size={20} className="text-blue-500" /> Recommended Resume Templates
          </h2>
          <div className="space-y-3">
            {analysis.template_recommendations.map((t, i) => (
              <div key={t.name} className={`p-4 rounded-xl border transition-all ${
                i === 0 
                  ? 'border-indigo-300 bg-gradient-to-br from-indigo-50 to-indigo-50/30 dark:from-indigo-900/30 dark:to-indigo-900/10' 
                  : 'border-slate-200 dark:border-slate-700 hover:border-slate-300'
              }`}>
                <div className="flex justify-between items-start gap-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-sm">{t.name}</h3>
                      {i === 0 && <span className="text-xs bg-indigo-600 text-white px-2 py-1 rounded-full font-medium">⭐ Best Match</span>}
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-2">{t.why_recommended}</p>
                    <div className="flex flex-wrap gap-1.5 mt-3">
                      {t.benefits.slice(0, 3).map((b) => (
                        <span key={b} className="inline-flex items-center gap-1 text-xs text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-2 py-1 rounded-lg">
                          <CheckCircle size={12} /> {b}
                        </span>
                      ))}
                      {t.benefits.length > 3 && (
                        <span className="text-xs text-slate-500 px-2 py-1">+{t.benefits.length - 3} more</span>
                      )}
                    </div>
                  </div>
                  {t.match_score !== undefined && (
                    <div className="text-right">
                      <div className="text-xl font-bold text-indigo-600">{t.match_score}%</div>
                      <p className="text-xs text-slate-500">Match</p>
                    </div>
                  )}
                </div>
                {t.description && (
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-3 pt-3 border-t border-slate-200 dark:border-slate-700">
                    {t.description}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Improvements */}
      <div className="card">
        <h2 className="font-semibold flex items-center gap-2 mb-4">
          <Lightbulb size={20} className="text-yellow-500" /> Improvement Suggestions
        </h2>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {analysis.improvements.map((tip, i) => (
            <li key={i} className="flex items-start gap-2 p-3 bg-yellow-50 dark:bg-yellow-900/10 rounded-xl text-sm">
              <span className="font-bold text-yellow-600">{i + 1}.</span> {tip}
            </li>
          ))}
        </ul>
      </div>

      {/* Skills + Roles */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-3">Skill Analysis</h2>
          <ResponsiveContainer width="100%" height={180}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Technical', value: analysis.analytics.skill_distribution.technical },
                  { name: 'Soft', value: analysis.analytics.skill_distribution.soft },
                ]}
                dataKey="value" cx="50%" cy="50%" outerRadius={70} label
              >
                {[0, 1].map((i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-2 mt-2">
            {analysis.skill_analysis.technical_skills.slice(0, 8).map((s) => (
              <span key={s} className="px-2 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-700 text-xs rounded-full">{s}</span>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="font-semibold flex items-center gap-2 mb-4">
            <Target size={20} className="text-purple-500" /> Career Role Predictions
          </h2>
          {analysis.role_predictions.map((r, i) => (
            <div key={r.role} className="flex items-center gap-3 mb-3">
              <span className="w-6 h-6 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-xs font-bold text-purple-600">{i + 1}</span>
              <div className="flex-1">
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">{r.role}</span>
                  <span className="text-purple-600 font-semibold">{r.confidence}%</span>
                </div>
                <div className="h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full">
                  <div className="h-full bg-purple-500 rounded-full" style={{ width: `${r.confidence}%` }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Jobs + Gap + Roadmap */}
      <div className="card">
        <h2 className="font-semibold flex items-center gap-2 mb-4">
          <Briefcase size={20} className="text-indigo-500" /> Job Recommendations
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {analysis.job_recommendations.map((job) => (
            <div key={job.title} className="p-4 bg-slate-50 dark:bg-slate-800 rounded-xl">
              <div className="flex justify-between mb-2">
                <h3 className="font-semibold text-sm">{job.title}</h3>
                <span className="text-indigo-600 font-bold">{job.match_percentage}%</span>
              </div>
              <p className="text-xs text-slate-500">{job.salary_range}</p>
              <p className="text-xs text-slate-500 mt-1">{job.career_path}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-3">Skill Gap — {analysis.skill_gap.target_role}</h2>
          <p className="text-sm text-green-600 font-medium mb-1">Matching</p>
          <div className="flex flex-wrap gap-1 mb-3">
            {analysis.skill_gap.matching_skills.map((s) => (
              <span key={s} className="px-2 py-0.5 bg-green-50 text-green-700 text-xs rounded">{s}</span>
            ))}
          </div>
          <p className="text-sm text-red-600 font-medium mb-1">Missing</p>
          <div className="flex flex-wrap gap-1">
            {analysis.skill_gap.missing_skills.map((s) => (
              <span key={s} className="px-2 py-0.5 bg-red-50 text-red-700 text-xs rounded">{s}</span>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="font-semibold flex items-center gap-2 mb-4">
            <BookOpen size={20} className="text-teal-500" /> Learning Roadmap
          </h2>
          {analysis.learning_roadmap.map((step) => (
            <div key={step.step} className="flex gap-3 mb-3">
              <div className="w-16 shrink-0 text-xs font-bold text-teal-600 pt-1">{step.month || `Step ${step.step}`}</div>
              <div>
                <p className="font-medium text-sm">{step.title}</p>
                <p className="text-xs text-slate-500">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Q&A + Cover Letter */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-3">Resume Q&A</h2>
          <div className="flex gap-2 mb-3">
            <input className="input text-sm" placeholder="What are my strongest skills?" value={qaQuestion} onChange={(e) => setQaQuestion(e.target.value)} />
            <button onClick={handleQA} className="btn-primary !px-4 text-sm">Ask</button>
          </div>
          {qaAnswer && <div className="p-3 bg-indigo-50 dark:bg-indigo-900/20 rounded-xl text-sm">{qaAnswer}</div>}
        </div>
        <div className="card">
          <h2 className="font-semibold mb-3">Cover Letter Generator</h2>
          <div className="flex gap-2 mb-3">
            <button onClick={handleCoverLetter} className="btn-secondary text-sm">Generate Cover Letter</button>
            {coverLetter && <button onClick={handleDownloadCoverLetter} className="btn-primary text-sm flex items-center gap-2"><Download size={16} /> Download</button>}
          </div>
          {coverLetter && <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-xl text-sm whitespace-pre-wrap max-h-48 overflow-y-auto">{coverLetter}</div>}
        </div>
      </div>

      {/* Interview Questions */}
      <div className="card">
        <h2 className="font-semibold mb-4">Interview Questions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(['easy', 'medium', 'hard'] as const).map((level) => (
            <div key={level}>
              <h3 className="text-sm font-medium capitalize text-slate-500 mb-2">{level}</h3>
              <ul className="space-y-1">
                {((analysis.interview_questions?.technical as Record<string, string[]>)?.[level] || []).map((q, i) => (
                  <li key={i} className="text-sm">{i + 1}. {q}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
