import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import AnalysisDashboard from '../components/AnalysisDashboard';
import LoadingSpinner from '../components/LoadingSpinner';
import { analysisApi } from '../services/api';
import type { AnalysisResult } from '../types';

export default function DashboardPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        if (id) {
          setAnalysis(await analysisApi.get(Number(id)));
        } else {
          const history = await analysisApi.history();
          if (history.length > 0) {
            setAnalysis(await analysisApi.get(history[0].id));
          } else {
            navigate('/upload');
          }
        }
      } catch {
        toast.error('Failed to load analysis');
        navigate('/upload');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id, navigate]);

  if (loading) return <LoadingSpinner>Analyzing your career profile...</LoadingSpinner>;
  if (!analysis) return null;

  return <AnalysisDashboard analysis={analysis} />;
}
