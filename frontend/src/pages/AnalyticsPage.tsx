import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, Radar,
} from 'recharts';
import LoadingSpinner from '../components/LoadingSpinner';
import ATSScoreRing from '../components/ATSScoreRing';
import { analysisApi } from '../services/api';
import type { AnalysisResult, ResumeHistoryItem } from '../types';

export default function AnalyticsPage() {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [history, setHistory] = useState<ResumeHistoryItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | ''>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    analysisApi.history().then((h) => {
      setHistory(h);
      if (h.length > 0) {
        setSelectedId(h[0].id);
        analysisApi.get(h[0].id).then(setAnalysis);
      }
    }).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (selectedId) analysisApi.get(Number(selectedId)).then(setAnalysis);
  }, [selectedId]);

  if (loading) return <LoadingSpinner>Loading analytics...</LoadingSpinner>;

  if (!analysis) {
    return (
      <div className="card text-center py-16">
        <p className="text-slate-500 mb-4">Upload a resume to see analytics</p>
        <Link to="/upload" className="btn-primary inline-block">Upload Resume</Link>
      </div>
    );
  }

  const radarData = Object.entries(analysis.ats_breakdown).map(([k, v]) => ({
    subject: k.charAt(0).toUpperCase() + k.slice(1),
    score: v,
    fullMark: 100,
  }));

  const trendData = history.slice(0, 5).reverse().map((h) => ({
    name: h.file_name.slice(0, 15),
    ats: h.ats_score || 0,
    readiness: h.career_readiness_score || 0,
  }));

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Analytics Dashboard</h1>
          <p className="text-slate-500">Track your resume performance over time</p>
        </div>
        {history.length > 1 && (
          <select className="input w-auto text-sm" value={selectedId} onChange={(e) => setSelectedId(Number(e.target.value))}>
            {history.map((h) => <option key={h.id} value={h.id}>{h.file_name}</option>)}
          </select>
        )}
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        {[
          { label: 'ATS Score', value: analysis.ats_score },
          { label: 'Resume Health', value: analysis.resume_health_score },
          { label: 'Career Readiness', value: analysis.career_readiness_score },
          { label: 'Job Match', value: analysis.job_match_percentage },
          { label: 'Template Rating', value: analysis.template_evaluation.rating * 10 },
        ].map(({ label, value }) => (
          <div key={label} className="card text-center !p-4">
            <p className="text-2xl font-bold text-indigo-600">{Math.round(value)}</p>
            <p className="text-xs text-slate-500 mt-1">{label}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card flex flex-col items-center">
          <h2 className="font-semibold mb-4 self-start">ATS Score</h2>
          <ATSScoreRing score={analysis.ats_score} />
          <p className="text-sm text-indigo-600 mt-4 font-medium">
            Top {analysis.analytics.industry_benchmark.percentile}% percentile
          </p>
        </div>
        <div className="card">
          <h2 className="font-semibold mb-4">Performance Radar</h2>
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11 }} />
              <Radar dataKey="score" stroke="#6366f1" fill="#6366f1" fillOpacity={0.3} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {trendData.length > 1 && (
        <div className="card">
          <h2 className="font-semibold mb-4">Score History</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis dataKey="name" tick={{ fontSize: 10 }} />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="ats" fill="#6366f1" name="ATS" radius={[4, 4, 0, 0]} />
              <Bar dataKey="readiness" fill="#8b5cf6" name="Readiness" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
