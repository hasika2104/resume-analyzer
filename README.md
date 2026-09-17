# AI Resume Analyzer, ATS Optimizer & Career Copilot

A production-ready AI-powered career platform that analyzes resumes, evaluates ATS compatibility, suggests templates, rewrites content with OpenAI GPT, recommends jobs, and provides an RAG-powered career assistant.

## Features

| Module | Description |
|--------|-------------|
| **Resume Upload** | PDF/DOCX parsing — name, contact, skills, education, experience, projects, certs, GitHub/LinkedIn |
| **ATS Score (0–100)** | Formatting, skills, experience, keywords, projects breakdown |
| **Template Evaluation** | Detects ATS-unfriendly layouts, columns, dense text |
| **Template Recommendations** | Role-based template suggestions with benefits |
| **AI Resume Rebuilder** | Before/after GPT rewrites of experience & projects |
| **Improvement Suggestions** | Actionable AI feedback |
| **Career Role Prediction** | 8+ roles with confidence scores |
| **Job Recommendations** | Match %, salary, career path, missing skills |
| **Skill Gap Analysis** | Current vs required skills |
| **Learning Roadmap** | Month-by-month personalized plan |
| **OpenAI Career Copilot** | RAG chatbot with resume context |
| **Resume Q&A** | Ask anything about your profile |
| **Cover Letter Generator** | GPT-powered cover letters |
| **Interview Questions** | Easy/Medium/Hard technical + behavioral |
| **Analytics Dashboard** | Health, readiness, benchmarks, score history |
| **Admin Dashboard** | Users, resumes, platform stats |
| **PDF Downloads** | Analysis report + improved resume |

## Tech Stack

React + TypeScript + Tailwind · FastAPI · PostgreSQL · OpenAI GPT · spaCy · NLTK · Sentence Transformers · pdfplumber · Recharts

## Quick Start

```bash
# Start PostgreSQL
docker compose up db -d

# Backend
cd backend && source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
# Add your OPENAI_API_KEY to .env
uvicorn app.main:app --reload
python seed.py

# Frontend
cd frontend && npm install && npm run dev
```

- **App:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs
- **Demo:** `demo@career.ai` / `demo123`
- **Admin:** `admin@career.ai` / `admin123`

## OpenAI Setup

Add to `backend/.env`:

```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```

Without an API key, the platform runs in rule-based fallback mode for all AI features.

## Docker

```bash
docker compose up --build -d
docker compose exec backend python seed.py
```

Frontend: http://localhost:3000

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/analysis/upload` | Upload & full analysis |
| `GET /api/analysis/{id}` | Get analysis |
| `POST /api/analysis/qa` | Resume Q&A |
| `POST /api/analysis/cover-letter` | Generate cover letter |
| `GET /api/analysis/{id}/download-improved` | Improved resume PDF |
| `POST /api/chat/` | Career Copilot (RAG) |
| `GET /api/admin/stats` | Admin analytics |

## License

MIT
