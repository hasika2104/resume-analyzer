import { useEffect, useState } from 'react';
import { Users, FileText, TrendingUp, Shield } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';
import { adminApi } from '../services/api';
import type { AdminStats, User } from '../types';

export default function AdminPage() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([adminApi.stats(), adminApi.users()])
      .then(([s, u]) => { setStats(s); setUsers(u); })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner>Loading admin dashboard...</LoadingSpinner>;
  if (!stats) return <div className="card text-center py-12">Access denied or failed to load.</div>;

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="flex items-center gap-3">
        <Shield className="text-indigo-600" size={28} />
        <div>
          <h1 className="text-2xl font-bold">Admin Dashboard</h1>
          <p className="text-slate-500">Platform management & analytics</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { label: 'Total Users', value: stats.total_users, icon: Users },
          { label: 'Resumes Analyzed', value: stats.total_resumes, icon: FileText },
          { label: 'Avg ATS Score', value: stats.average_ats_score, icon: TrendingUp },
        ].map(({ label, value, icon: Icon }) => (
          <div key={label} className="card flex items-center gap-4">
            <div className="p-3 bg-indigo-100 dark:bg-indigo-900/30 rounded-xl">
              <Icon className="text-indigo-600" size={24} />
            </div>
            <div>
              <p className="text-2xl font-bold">{value}</p>
              <p className="text-sm text-slate-500">{label}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-4">Role Distribution</h2>
          <div className="space-y-2">
            {Object.entries(stats.role_distribution).map(([role, count]) => (
              <div key={role} className="flex justify-between text-sm">
                <span>{role}</span>
                <span className="font-semibold">{count}</span>
              </div>
            ))}
            {Object.keys(stats.role_distribution).length === 0 && (
              <p className="text-slate-500 text-sm">No data yet</p>
            )}
          </div>
        </div>

        <div className="card">
          <h2 className="font-semibold mb-4">Recent Uploads</h2>
          <div className="space-y-2">
            {stats.recent_uploads.map((r) => (
              <div key={r.id} className="flex justify-between text-sm p-2 bg-slate-50 dark:bg-slate-800 rounded-lg">
                <span className="truncate">{r.file_name}</span>
                <span className="text-indigo-600 font-medium shrink-0 ml-2">{r.ats_score}/100</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card overflow-x-auto">
        <h2 className="font-semibold mb-4">Users ({users.length})</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 dark:border-slate-800">
              <th className="text-left py-2 px-3 text-slate-500">Name</th>
              <th className="text-left py-2 px-3 text-slate-500">Email</th>
              <th className="text-left py-2 px-3 text-slate-500">Admin</th>
              <th className="text-left py-2 px-3 text-slate-500">Joined</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-b border-slate-100 dark:border-slate-800">
                <td className="py-2 px-3">{u.full_name}</td>
                <td className="py-2 px-3">{u.email}</td>
                <td className="py-2 px-3">{u.is_admin ? 'Yes' : 'No'}</td>
                <td className="py-2 px-3">{new Date(u.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
