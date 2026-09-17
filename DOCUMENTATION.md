# Project Documentation: AI Resume Analyzer & Career Copilot

## Overview

This project is an AI-powered ATS Resume Analyzer and Career Copilot platform built with React, TypeScript, FastAPI, PostgreSQL, spaCy, and OpenAI.

---

## Files & Folder Structure

```
resume analyzer/
├── PROJECT_REPORT.md       # Full technical report & architecture documentation
├── DOCUMENTATION.md        # Project guide & API documentation (This file)
├── README.md               # Quickstart guide & environment setup
├── docker-compose.yml      # Multi-container Docker configuration
├── sql/
│   └── init.sql            # PostgreSQL database initialization script
├── backend/
│   ├── app/
│   │   ├── main.py         # FastAPI main entrypoint
│   │   ├── database.py     # SQLAlchemy DB connection & sessions
│   │   ├── config.py       # Pydantic settings & environment configuration
│   │   ├── models/         # SQLAlchemy database models (User, Resume, Chat)
│   │   ├── routers/        # API route handlers (auth, analysis, chat, admin)
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── services/       # Core business logic & algorithms (ATS scoring, parser, OpenAI, career copilot)
│   │   └── utils/          # Helper modules (auth JWT, text extraction)
│   ├── requirements.txt    # Python backend dependencies
│   └── seed.py             # Database seed script for initial demo data
└── frontend/
    ├── src/
    │   ├── App.tsx         # React application router & root component
    │   ├── main.tsx        # Vite React DOM entrypoint
    │   ├── components/     # UI components (ATS Score ring, dashboards, file uploader)
    │   ├── pages/          # Application views (Upload, Dashboard, History, Compare, Chat, Admin)
    │   ├── context/        # Auth & Theme state contexts
    │   └── services/       # Axios API client module
    ├── package.json        # Frontend Node.js dependencies
    └── vite.config.ts      # Vite build & server configuration
```

---

## Quick Running Guide

1. **Database**: PostgreSQL on `localhost:5432` (`ats_db`)
2. **Backend Server**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
3. **Frontend Application**:
   ```bash
   cd frontend
   npm run dev
   ```

- Access Frontend: `http://localhost:5173`
- Access API Docs: `http://localhost:8000/docs`
- Public GitHub: [https://github.com/ippilihasika/resume-analyzer](https://github.com/ippilihasika/resume-analyzer)
