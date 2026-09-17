import axios from 'axios';
import type { User, AnalysisResult, ResumeHistoryItem, ChatMessage, AdminStats } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || '/api';
const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (email: string, password: string) => {
    const form = new URLSearchParams();
    form.append('username', email);
    form.append('password', password);
    const { data } = await api.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return data as { access_token: string; user: User };
  },
  signup: async (email: string, password: string, full_name: string) => {
    const { data } = await api.post('/auth/signup', { email, password, full_name });
    return data as User;
  },
  me: async () => {
    const { data } = await api.get('/auth/me');
    return data as User;
  },
};

export const analysisApi = {
  upload: async (file: File) => {
    const form = new FormData();
    form.append('file', file);
    const { data } = await api.post('/analysis/upload', form);
    return data as AnalysisResult;
  },
  get: async (id: number) => {
    const { data } = await api.get(`/analysis/${id}`);
    return data as AnalysisResult;
  },
  history: async () => {
    const { data } = await api.get('/analysis/history');
    return data as ResumeHistoryItem[];
  },
  delete: async (id: number) => await api.delete(`/analysis/${id}`),
  downloadPdf: async (id: number) => {
    const { data } = await api.get(`/analysis/${id}/download-pdf`, { responseType: 'blob' });
    return data as Blob;
  },
  compare: async (resumeIds: number[]) => {
    const { data } = await api.post('/analysis/compare', { resume_ids: resumeIds });
    return data;
  },
  qa: async (resumeId: number, question: string) => {
    const { data } = await api.post('/analysis/qa', { resume_id: resumeId, question });
    return data as { question: string; answer: string };
  },
  coverLetter: async (resumeId: number, targetRole?: string) => {
    const { data } = await api.post('/analysis/cover-letter', {
      resume_id: resumeId,
      target_role: targetRole,
    });
    return data as { target_role: string; cover_letter: string };
  },
  downloadCoverLetter: async (resumeId: number, targetRole?: string) => {
    const { data } = await api.post(`/analysis/${resumeId}/download-cover-letter`, {
      resume_id: resumeId,
      target_role: targetRole,
    }, { responseType: 'blob' });
    return data as Blob;
  },
};

export const chatApi = {
  send: async (message: string, resumeId?: number) => {
    const { data } = await api.post('/chat/', { message, resume_id: resumeId });
    return data as ChatMessage;
  },
  history: async () => {
    const { data } = await api.get('/chat/history');
    return data as ChatMessage[];
  },
  status: async () => {
    const { data } = await api.get('/chat/status');
    return data as { openai_enabled: boolean };
  },
};

export const adminApi = {
  stats: async () => {
    const { data } = await api.get('/admin/stats');
    return data as AdminStats;
  },
  users: async () => {
    const { data } = await api.get('/admin/users');
    return data as User[];
  },
  resumes: async () => {
    const { data } = await api.get('/admin/resumes');
    return data;
  },
};

export default api;
