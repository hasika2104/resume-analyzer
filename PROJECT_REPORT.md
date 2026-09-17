# AI Resume Analyzer, ATS Optimizer & Career Copilot
## Comprehensive Project Documentation & Technical Report

---

### Executive Summary

**AI Resume Analyzer, ATS Optimizer & Career Copilot** is an enterprise-grade, full-stack career platform designed to evaluate resumes against modern Applicant Tracking Systems (ATS), provide actionable AI-driven optimization advice, predict career trajectories, and supply candidates with personalized learning roadmaps and interview preparation tools.

The platform combines deterministic NLP extraction (**spaCy**, **pdfplumber**, **NLTK**, **Sentence Transformers**) with generative AI (**OpenAI GPT-4o**) for hybrid evaluation—enabling instant fallback to rule-based algorithms when AI services are offline or rate-limited.

---

### Key System Capabilities

| Feature Module | Description & Business Value |
| :--- | :--- |
| **PDF & DOCX Parsing** | Automatic extraction of contact details, skills, work experience, projects, education, certifications, GitHub, and LinkedIn profiles. |
| **Multi-Dimensional ATS Scoring** | Weighted 0–100 scoring evaluating formatting, keyword density, skill relevance, structural balance, and project complexity. |
| **Template Compatibility Engine** | Identifies layout flaws such as multi-column structures, tables, text overload, and ATS-unfriendly font hierarchy. |
| **AI Resume Rebuilder** | Provides side-by-side (before/after) bullet-point rewrites using action verbs and quantified impact metrics via GPT-4o. |
| **Career Role Prediction** | Evaluates candidate fit across 8+ specialized tech roles with percentage confidence scores. |
| **Job Match & Skill Gap Analysis** | Compares extracted profile against target role requirements, calculating skill gaps and salary benchmark targets. |
| **Interactive Learning Roadmap** | Generates month-by-month actionable skill acquisition milestones. |
| **Career Copilot (RAG Chatbot)** | Context-aware assistant allowing users to query their uploaded resume data and receive tailored career advice. |
| **PDF Report Generation** | Exportable, high-impact PDF reports containing full analysis and improved resume layouts. |
| **Admin Analytics Dashboard** | System-wide statistics monitoring total users, average ATS scores, top missing skills, and platform health. |

---

### Architecture & System Overview

```
+-------------------------------------------------------------+
|               React + TypeScript Frontend                   |
|              (Vite, TailwindCSS, Recharts)                  |
+------------------------------+------------------------------+
                               | REST Requests & JWT
                               v
+-------------------------------------------------------------+
|                    FastAPI Backend Server                   |
|                    (Uvicorn, REST API)                      |
+-------+----------------------+----------------------+-------+
        | ORM                  | Extract & Score      | RAG / GPT
        v                      v                      v
+---------------+      +---------------+      +---------------+
| PostgreSQL DB |      | NLP Engine    |      | OpenAI GPT-4o |
|   (ats_db)    |      | (spaCy/NLTK)  |      |   (AI API)    |
+---------------+      +---------------+      +---------------+
```

---

### Tech Stack Specifications

#### Frontend Architecture
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 6
- **Styling**: TailwindCSS + Custom CSS glassmorphism components
- **State Management & Auth**: React Context API (`AuthContext`, `ThemeContext`)
- **Data Visualization**: Recharts (radar charts, score breakdown rings, trend line graphs)
- **Icons**: Lucide React

#### Backend Architecture
- **Framework**: Python 3.12 + FastAPI
- **Server**: Uvicorn ASGI Server
- **ORM & DB Connection**: SQLAlchemy Declarative Models + Session Pooling
- **Security & Authentication**: JWT (JSON Web Tokens) with Passlib & PyJWT
- **Document Processing**: `pdfplumber`, `python-docx`
- **Natural Language Processing**: `spaCy` (`en_core_web_sm`), `nltk`

#### Database & Infrastructure
- **Database**: PostgreSQL 16
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git & GitHub (`ippilihasika/resume-analyzer`)

---

### ATS Scoring Algorithm & Weights

The platform employs a deterministic scoring model that evaluates resumes across multiple categories to yield a final **0–100 ATS Score**:

$$\text{ATS Score} = \sum_{k \in K} \text{Score}(k) \times \text{Weight}(k)$$

#### Category Weight Distribution

| Category | Weight | Description |
| :--- | :---: | :--- |
| **Skills Coverage** | `20%` | Frequency, diversity, and categorization of technical & soft skills. |
| **Work Experience** | `20%` | Measurable accomplishments, action verb density, and chronology. |
| **Formatting & Layout** | `15%` | Text density, section headers, font consistency, and clean structure. |
| **Keywords Match** | `15%` | Alignment with target role terminology and industry keywords. |
| **Projects Complexity** | `15%` | Inclusion of tech stacks, outcomes, and repository links. |
| **Section Structure** | `5%` | Presence of essential sections (Skills, Experience, Education). |
| **Contact Completeness** | `5%` | Detection of name, email, phone number, location, and profiles. |
| **Readability** | `5%` | Flesch readability index and bullet point length distribution. |

---

### Database Schema (PostgreSQL)

#### `users` Table
- `id`: `INTEGER PRIMARY KEY`
- `email`: `VARCHAR(255) UNIQUE NOT NULL`
- `hashed_password`: `VARCHAR(255) NOT NULL`
- `full_name`: `VARCHAR(255) NOT NULL`
- `is_active`: `BOOLEAN DEFAULT TRUE`
- `is_admin`: `BOOLEAN DEFAULT FALSE`
- `created_at`: `TIMESTAMP`

#### `resumes` Table
- `id`: `INTEGER PRIMARY KEY`
- `user_id`: `INTEGER FOREIGN KEY -> users(id)`
- `file_name`: `VARCHAR(255)`
- `file_path`: `VARCHAR(500)`
- `raw_text`: `TEXT`
- `parsed_data`: `JSON`
- `ats_score`: `FLOAT`
- `ats_breakdown`: `JSON`
- `role_predictions`: `JSON`
- `job_recommendations`: `JSON`
- `learning_roadmap`: `JSON`
- `resume_rewrites`: `JSON`
- `created_at`: `TIMESTAMP`

#### `chat_messages` Table
- `id`: `INTEGER PRIMARY KEY`
- `user_id`: `INTEGER FOREIGN KEY -> users(id)`
- `role`: `VARCHAR(20)` (`user` | `assistant`)
- `content`: `TEXT`
- `created_at`: `TIMESTAMP`

---

### API Endpoint Summary

| HTTP Method | Endpoint Path | Description | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register new user account | Public |
| `POST` | `/api/auth/login` | Authenticate user & obtain JWT token | Public |
| `GET` | `/api/auth/me` | Fetch authenticated user profile | Bearer Token |
| `POST` | `/api/analysis/upload` | Upload resume file (PDF/DOCX) & trigger full analysis | Bearer Token |
| `GET` | `/api/analysis/{id}` | Retrieve comprehensive analysis results by ID | Bearer Token |
| `POST` | `/api/analysis/qa` | Execute specific Q&A queries against parsed resume | Bearer Token |
| `POST` | `/api/analysis/cover-letter` | Generate AI customized cover letter | Bearer Token |
| `POST` | `/api/chat/` | Send message to RAG Career Copilot | Bearer Token |
| `GET` | `/api/admin/stats` | Retrieve platform-wide analytics and performance metrics | Admin Token |

---

### Execution & Running Instructions

#### Prerequisites
- **Python**: 3.10+
- **Node.js**: 18+
- **PostgreSQL**: 14+ running locally on port `5432` or via Docker Compose.

#### Step 1: Start PostgreSQL
```bash
docker compose up db -d
```

#### Step 2: Backend Setup & Launch
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 3: Frontend Launch
```bash
cd frontend
npm install
npm run dev
```

- **Frontend Application**: `http://localhost:5173`
- **Interactive API Docs**: `http://localhost:8000/docs`

---

### Public Repository & Links

- **GitHub Repository**: [https://github.com/ippilihasika/resume-analyzer](https://github.com/ippilihasika/resume-analyzer)
- **Default Seed Accounts**:
  - User Demo: `demo@career.ai` / `demo123`
  - Admin Demo: `admin@career.ai` / `admin123`
