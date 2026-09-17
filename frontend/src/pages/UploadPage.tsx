import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import { analysisApi } from '../services/api';

export default function UploadPage() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async (files: File[]) => {
    if (files.length !== 1) {
      toast.error('Please upload one resume at a time');
      return;
    }
    setLoading(true);
    try {
      const result = await analysisApi.upload(files[0]);
      toast.success(`Analysis complete! ATS Score: ${result.ats_score}/100`);
      navigate(`/dashboard/${result.id}`);
    } catch {
      toast.error('Failed to analyze resume. Please upload a valid PDF or DOCX.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <LoadingSpinner>
        <p className="mt-4 text-lg font-medium">Analyzing your resume...</p>
        <p className="text-sm text-slate-500 mt-2">Extracting skills, computing ATS score, predicting roles</p>
      </LoadingSpinner>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8 animate-fade-in-up">
      <div className="text-center">
        <h1 className="text-3xl font-bold">Upload Your Resume</h1>
        <p className="text-slate-500 mt-2">
          Get instant ATS score, career recommendations, and a personalized learning roadmap
        </p>
      </div>

      <div className="card">
        <FileUpload onUpload={handleUpload} loading={loading} multiple={false} />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
        {[
          { title: 'ATS Score', desc: '0–100 compatibility rating' },
          { title: 'Career Match', desc: 'Role predictions with confidence' },
          { title: 'Learning Path', desc: 'Personalized skill roadmap' },
        ].map(({ title, desc }) => (
          <div key={title} className="card !p-4">
            <p className="font-semibold text-sm">{title}</p>
            <p className="text-xs text-slate-500 mt-1">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
