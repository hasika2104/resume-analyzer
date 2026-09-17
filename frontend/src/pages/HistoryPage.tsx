import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Trash2, FileText } from 'lucide-react';
import toast from 'react-hot-toast';
import LoadingSpinner from '../components/LoadingSpinner';
import ATSScoreRing from '../components/ATSScoreRing';
import { analysisApi } from '../services/api';
import type { ResumeHistoryItem } from '../types';

export default function HistoryPage() {
  const [history, setHistory] = useState<ResumeHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    analysisApi.history().then(setHistory).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this resume analysis?')) return;
    await analysisApi.delete(id);
    toast.success('Deleted');
    load();
  };

  if (loading) return <LoadingSpinner>Loading history...</LoadingSpinner>;

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div>
        <h1 className="text-2xl font-bold">Resume History</h1>
        <p className="text-slate-500 mt-1">View and manage your past resume analyses</p>
      </div>

      {history.length === 0 ? (
        <div className="card text-center py-16">
          <FileText className="mx-auto text-slate-300 mb-4" size={48} />
          <p className="text-slate-500">No resumes analyzed yet</p>
          <Link to="/upload" className="btn-primary inline-block mt-4">Upload Resume</Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {history.map((item) => (
            <div key={item.id} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold truncate">{item.file_name}</h3>
                  <p className="text-xs text-slate-500 mt-1">
                    {new Date(item.created_at).toLocaleDateString()}
                  </p>
                  {item.top_role && (
                    <span className="inline-block mt-2 px-2 py-0.5 bg-purple-50 dark:bg-purple-900/30 text-purple-700 text-xs rounded-full">
                      {item.top_role}
                    </span>
                  )}
                </div>
                {item.ats_score != null && <ATSScoreRing score={item.ats_score} size={80} />}
              </div>
              <div className="flex gap-2 mt-4">
                <Link to={`/dashboard/${item.id}`} className="btn-primary flex-1 text-center text-sm !py-2">
                  View Analysis
                </Link>
                <button onClick={() => handleDelete(item.id)} className="p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl">
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
