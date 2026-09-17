import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import LoadingSpinner from '../components/LoadingSpinner';
import { analysisApi } from '../services/api';
import type { ResumeHistoryItem } from '../types';

interface CompareItem {
  id: number;
  file_name: string;
  ats_score: number;
  top_role: string | null;
  skills_count: number;
  skill_strength: number;
}

export default function ComparePage() {
  const [history, setHistory] = useState<ResumeHistoryItem[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [comparison, setComparison] = useState<CompareItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [comparing, setComparing] = useState(false);

  useEffect(() => {
    analysisApi.history().then(setHistory).finally(() => setLoading(false));
  }, []);

  const toggle = (id: number) => {
    setSelected((prev) => {
      if (prev.includes(id)) return prev.filter((x) => x !== id);
      if (prev.length >= 5) { toast.error('Max 5 resumes'); return prev; }
      return [...prev, id];
    });
  };

  const handleCompare = async () => {
    if (selected.length < 2) { toast.error('Select at least 2 resumes'); return; }
    setComparing(true);
    try {
      const data = await analysisApi.compare(selected);
      setComparison(data.resumes);
    } catch {
      toast.error('Comparison failed');
    } finally {
      setComparing(false);
    }
  };

  if (loading) return <LoadingSpinner>Loading...</LoadingSpinner>;

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div>
        <h1 className="text-2xl font-bold">Compare Resumes</h1>
        <p className="text-slate-500 mt-1">Select 2–5 resumes to compare side by side</p>
      </div>

      <div className="card">
        <div className="flex flex-wrap gap-2 mb-4">
          {history.map((h) => (
            <button
              key={h.id}
              onClick={() => toggle(h.id)}
              className={`px-4 py-2 rounded-xl text-sm border transition ${
                selected.includes(h.id)
                  ? 'bg-indigo-50 border-indigo-500 text-indigo-700 dark:bg-indigo-900/30'
                  : 'border-slate-300 dark:border-slate-700 hover:border-indigo-400'
              }`}
            >
              {h.file_name} {h.ats_score != null && `(${h.ats_score})`}
            </button>
          ))}
        </div>
        {history.length < 2 && <p className="text-slate-500 text-sm">Upload at least 2 resumes to compare.</p>}
        <button onClick={handleCompare} disabled={selected.length < 2 || comparing} className="btn-primary">
          {comparing ? 'Comparing...' : `Compare ${selected.length} Resumes`}
        </button>
      </div>

      {comparison.length > 0 && (
        <div className="card overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800">
                <th className="text-left py-3 px-4 text-sm text-slate-500">Metric</th>
                {comparison.map((c) => (
                  <th key={c.id} className="text-left py-3 px-4 text-sm font-medium">{c.file_name}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                ['ATS Score', (c: CompareItem) => `${c.ats_score}/100`],
                ['Top Role', (c: CompareItem) => c.top_role || '—'],
                ['Skills Count', (c: CompareItem) => String(c.skills_count)],
                ['Skill Strength', (c: CompareItem) => `${c.skill_strength}/100`],
              ].map(([label, fn]) => (
                <tr key={label as string} className="border-b border-slate-100 dark:border-slate-800">
                  <td className="py-3 px-4 text-sm text-slate-500">{label as string}</td>
                  {comparison.map((c) => (
                    <td key={c.id} className="py-3 px-4 font-medium">{(fn as (c: CompareItem) => string)(c)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
