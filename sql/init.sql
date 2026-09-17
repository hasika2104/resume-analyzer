-- AI Resume Analyzer & Career Recommendation Platform
-- PostgreSQL Schema v2.0

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    raw_text TEXT,
    parsed_data JSONB,
    ats_score FLOAT,
    ats_breakdown JSONB,
    resume_health_score FLOAT,
    career_readiness_score FLOAT,
    job_match_percentage FLOAT,
    ai_summary TEXT,
    improvements JSONB,
    skill_analysis JSONB,
    role_predictions JSONB,
    job_recommendations JSONB,
    skill_gap JSONB,
    learning_roadmap JSONB,
    interview_questions JSONB,
    template_evaluation JSONB,
    template_recommendations JSONB,
    resume_rewrites JSONB,
    analytics JSONB,
    improved_content JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_resumes_user ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_resumes_ats ON resumes(ats_score DESC);

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_messages(user_id);

-- Run: python seed.py
