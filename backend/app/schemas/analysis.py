from datetime import datetime
from pydantic import BaseModel, Field


class ResumeListItem(BaseModel):
    id: int
    file_name: str
    ats_score: float | None
    ai_summary: str | None
    top_role: str | None = None
    career_readiness_score: float | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ATSBreakdown(BaseModel):
    formatting: float = 0
    skills: float = 0
    experience: float = 0
    keywords: float = 0
    projects: float = 0


class TemplateEvaluation(BaseModel):
    rating: float
    problems: list[str]
    ats_friendly: bool
    readability_score: float


class TemplateRecommendation(BaseModel):
    name: str
    description: str
    benefits: list[str]
    preview_style: str
    why_recommended: str


class ResumeRewrite(BaseModel):
    section: str
    before: str
    after: str


class SkillAnalysis(BaseModel):
    all_skills: list[str]
    technical_skills: list[str]
    soft_skills: list[str]
    skill_strength_score: float


class RolePrediction(BaseModel):
    role: str
    confidence: float


class JobRecommendation(BaseModel):
    title: str
    match_percentage: float
    missing_skills: list[str]
    salary_range: str
    career_path: str
    learning_requirements: list[str] = []


class SkillGap(BaseModel):
    current_skills: list[str]
    target_role: str
    missing_skills: list[str]
    matching_skills: list[str]


class RoadmapStep(BaseModel):
    step: int
    month: str | None = None
    title: str
    description: str
    resources: list[str] = []


class AnalyticsDashboard(BaseModel):
    ats_score: float
    resume_health_score: float
    career_readiness_score: float
    job_match_percentage: float
    skill_distribution: dict
    industry_benchmark: dict
    top_role: str | None = None
    top_role_confidence: float = 0


class AnalysisResponse(BaseModel):
    id: int
    file_name: str
    parsed_data: dict
    ats_score: float
    ats_breakdown: ATSBreakdown
    resume_health_score: float
    career_readiness_score: float
    job_match_percentage: float
    ai_summary: str
    improvements: list[str]
    skill_analysis: SkillAnalysis
    role_predictions: list[RolePrediction]
    job_recommendations: list[JobRecommendation]
    skill_gap: SkillGap
    learning_roadmap: list[RoadmapStep]
    interview_questions: dict
    template_evaluation: TemplateEvaluation
    template_recommendations: list[TemplateRecommendation]
    resume_rewrites: list[ResumeRewrite]
    analytics: AnalyticsDashboard
    openai_enabled: bool = False
    created_at: datetime


class CompareRequest(BaseModel):
    resume_ids: list[int] = Field(min_length=2, max_length=5)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    resume_id: int | None = None


class QARequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    resume_id: int


class CoverLetterRequest(BaseModel):
    resume_id: int
    target_role: str | None = None


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
