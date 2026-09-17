export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

export interface ATSBreakdown {
  formatting: number;
  skills: number;
  experience: number;
  keywords: number;
  projects: number;
}

export interface TemplateEvaluation {
  rating: number;
  problems: string[];
  ats_friendly: boolean;
  readability_score: number;
}

export interface TemplateRecommendation {
  name: string;
  description: string;
  benefits: string[];
  preview_style: string;
  why_recommended: string;
  match_score?: number;
}

export interface ResumeRewrite {
  section: string;
  before: string;
  after: string;
}

export interface SkillAnalysis {
  all_skills: string[];
  technical_skills: string[];
  soft_skills: string[];
  skill_strength_score: number;
}

export interface RolePrediction {
  role: string;
  confidence: number;
}

export interface JobRecommendation {
  title: string;
  match_percentage: number;
  missing_skills: string[];
  salary_range: string;
  career_path: string;
  learning_requirements?: string[];
}

export interface SkillGap {
  current_skills: string[];
  target_role: string;
  missing_skills: string[];
  matching_skills: string[];
}

export interface RoadmapStep {
  step: number;
  month?: string;
  title: string;
  description: string;
  resources: string[];
}

export interface AnalyticsDashboard {
  ats_score: number;
  resume_health_score: number;
  career_readiness_score: number;
  job_match_percentage: number;
  skill_distribution: { technical: number; soft: number; total: number };
  industry_benchmark: {
    your_ats: number;
    industry_avg_ats: number;
    your_health: number;
    industry_avg_health: number;
    your_readiness: number;
    industry_avg_readiness: number;
    percentile: number;
  };
  top_role?: string;
  top_role_confidence?: number;
}

export interface AnalysisResult {
  id: number;
  file_name: string;
  parsed_data: Record<string, unknown>;
  ats_score: number;
  ats_breakdown: ATSBreakdown;
  resume_health_score: number;
  career_readiness_score: number;
  job_match_percentage: number;
  ai_summary: string;
  improvements: string[];
  skill_analysis: SkillAnalysis;
  role_predictions: RolePrediction[];
  job_recommendations: JobRecommendation[];
  skill_gap: SkillGap;
  learning_roadmap: RoadmapStep[];
  interview_questions: Record<string, unknown>;
  template_evaluation: TemplateEvaluation;
  template_recommendations: TemplateRecommendation[];
  resume_rewrites: ResumeRewrite[];
  analytics: AnalyticsDashboard;
  openai_enabled: boolean;
  created_at: string;
}

export interface ResumeHistoryItem {
  id: number;
  file_name: string;
  ats_score: number | null;
  ai_summary: string | null;
  top_role: string | null;
  career_readiness_score: number | null;
  created_at: string;
}

export interface ChatMessage {
  id: number;
  role: string;
  content: string;
  created_at: string;
}

export interface AdminStats {
  total_users: number;
  total_resumes: number;
  average_ats_score: number;
  role_distribution: Record<string, number>;
  recent_uploads: { id: number; file_name: string; ats_score: number; user_id: number; created_at: string }[];
}

// Interview Coach Types
export interface InterviewQuestion {
  question: string;
  answer: string;
  difficulty: string;
}

export interface ProjectQuestions {
  architecture: InterviewQuestion[];
  data_flow: InterviewQuestion[];
  database: InterviewQuestion[];
  api: InterviewQuestion[];
  deployment: InterviewQuestion[];
  challenges: InterviewQuestion[];
}

export interface SkillGapData {
  target_role: string;
  current_skills_count: number;
  essential: { present: string[]; missing: string[] };
  recommended: { present: string[]; missing: string[] };
  nice_to_have: { present: string[]; missing: string[] };
}

export interface DSARoadmap {
  difficulty_level: string;
  arrays: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
  strings: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
  hashing: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
  linked_lists: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
  stacks_queues: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
  trees: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
  graphs: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
  dynamic_programming: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
  recursion: { importance: string; topics: string[]; frequency: string; expected_difficulty: string; problems: string[] };
}

export interface PreparationPlan {
  duration_days: number;
  weeks: number;
  difficulty_level: string;
  weekly_schedule: Array<{
    week: number;
    topics: string[];
    hours: number;
    target_problems: number;
  }>;
}

export interface CompanyPrep {
  company_type: string;
  focus_areas: string[];
  interview_rounds: Array<{
    round: string;
    duration: string;
    focus: string;
  }>;
  tips: string[];
}

export interface InterviewReadinessScore {
  total_score: number;
  max_score: number;
  percentage: number;
  readiness_level: string;
  breakdown: Record<string, number>;
  strengths: string[];
  areas_to_improve: string[];
}

export interface ProjectEnhancement {
  project_name: string;
  current_features: string[];
  advanced_features: string[];
  ai_integration_opportunities: string[];
  cloud_deployment: string[];
  production_improvements: string[];
  monetization_strategies: string[];
  interviewer_impressive_features: string[];
}

export interface InterviewCoachRoadmap {
  resume_analysis: {
    tech_stack: Record<string, string[]>;
    total_skills: number;
    projects_count: number;
    experience_years: number;
  };
  technical_questions: Record<string, string[]>;
  skill_gap_analysis: SkillGapData;
  dsa_roadmap: DSARoadmap;
  interview_readiness_score: InterviewReadinessScore;
  projects_analysis: Array<{
    project: string;
    questions: ProjectQuestions;
    enhancements: ProjectEnhancement;
  }>;
}
