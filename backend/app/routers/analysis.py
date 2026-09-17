from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.schemas.analysis import (
    AnalysisResponse, ResumeListItem, CompareRequest, QARequest, CoverLetterRequest,
)
from app.services.resume_parser import parse_resume
from app.services.ats_scoring_service import compute_ats_score
from app.services.career_service import (
    predict_roles, generate_job_recommendations, analyze_skill_gap,
    generate_learning_roadmap, generate_skill_analysis,
)
from app.services.template_service import evaluate_template, recommend_templates
from app.services.analytics_service import compute_analytics
from app.services.openai_service import (
    is_openai_available, generate_ai_summary_gpt, generate_improvements_gpt,
    rewrite_resume_sections, generate_interview_questions_gpt, generate_cover_letter,
    answer_resume_qa, build_resume_context,
)
from app.services.report_service import generate_analysis_pdf, generate_cover_letter_pdf
from app.utils.auth import get_current_user
from app.utils.file_handler import save_upload_file
from app.utils.text_extractor import extract_text_from_resume, clean_text

router = APIRouter(prefix="/analysis", tags=["Resume Analysis"])


def _run_full_analysis(raw_text: str, file_path: str | None = None, file_type: str = "pdf") -> dict:
    parsed = parse_resume(raw_text)
    
    # Calculate experience years
    experience = parsed.get("experience", [])
    experience_years = len(experience) * 1.5  # rough estimate: ~1.5 years per position
    
    ats_result = compute_ats_score(parsed, raw_text)
    ats_score = ats_result["ats_score"]
    ats_breakdown = ats_result["ats_breakdown"]

    role_predictions = predict_roles(parsed)
    job_recommendations = generate_job_recommendations(role_predictions, parsed)
    for rec in job_recommendations:
        rec["learning_requirements"] = rec.get("missing_skills", [])[:4]

    target_role = role_predictions[0]["role"] if role_predictions else "Software Engineer"
    skill_gap = analyze_skill_gap(parsed, target_role)
    learning_roadmap = generate_learning_roadmap(target_role, skill_gap, experience_years, parsed)
    skill_analysis = generate_skill_analysis(parsed)

    template_eval = evaluate_template(raw_text, file_path, file_type)
    template_recs = recommend_templates(parsed, role_predictions)
    resume_rewrites = rewrite_resume_sections(parsed)

    improvements = generate_improvements_gpt(parsed, ats_breakdown)
    ai_summary = generate_ai_summary_gpt(parsed, role_predictions)
    interview_questions = generate_interview_questions_gpt(parsed, experience_years)

    analytics = compute_analytics(
        parsed, ats_score, ats_breakdown, skill_analysis,
        role_predictions, job_recommendations, template_eval["rating"],
    )

    improved_content = {
        "summary": ai_summary,
        "rewrites": resume_rewrites,
        "recommended_template": template_recs[0]["name"] if template_recs else "Modern ATS Professional",
    }

    return {
        "parsed_data": parsed,
        "ats_score": ats_score,
        "ats_breakdown": ats_breakdown,
        "resume_health_score": analytics["resume_health_score"],
        "career_readiness_score": analytics["career_readiness_score"],
        "job_match_percentage": analytics["job_match_percentage"],
        "ai_summary": ai_summary,
        "improvements": improvements,
        "skill_analysis": skill_analysis,
        "role_predictions": role_predictions,
        "job_recommendations": job_recommendations,
        "skill_gap": skill_gap,
        "learning_roadmap": learning_roadmap,
        "interview_questions": interview_questions,
        "template_evaluation": template_eval,
        "template_recommendations": template_recs,
        "resume_rewrites": resume_rewrites,
        "analytics": analytics,
        "improved_content": improved_content,
    }


def _to_response(resume: Resume) -> AnalysisResponse:
    return AnalysisResponse(
        id=resume.id,
        file_name=resume.file_name,
        parsed_data=resume.parsed_data or {},
        ats_score=resume.ats_score or 0,
        ats_breakdown=resume.ats_breakdown or {},
        resume_health_score=resume.resume_health_score or 0,
        career_readiness_score=resume.career_readiness_score or 0,
        job_match_percentage=resume.job_match_percentage or 0,
        ai_summary=resume.ai_summary or "",
        improvements=resume.improvements or [],
        skill_analysis=resume.skill_analysis or {},
        role_predictions=resume.role_predictions or [],
        job_recommendations=resume.job_recommendations or [],
        skill_gap=resume.skill_gap or {},
        learning_roadmap=resume.learning_roadmap or [],
        interview_questions=resume.interview_questions or {},
        template_evaluation=resume.template_evaluation or {},
        template_recommendations=resume.template_recommendations or [],
        resume_rewrites=resume.resume_rewrites or [],
        analytics=resume.analytics or {},
        openai_enabled=is_openai_available(),
        created_at=resume.created_at,
    )


@router.post("/upload", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def upload_and_analyze(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
):
    file_name, file_path, file_type = await save_upload_file(file)
    raw_text = clean_text(extract_text_from_resume(file_path, file_type))

    if len(raw_text) < 50:
        raise HTTPException(status_code=400, detail="Could not extract enough text from the resume.")

    analysis = _run_full_analysis(raw_text, file_path, file_type)

    resume = Resume(
        user_id=current_user.id,
        file_name=file.filename or file_name,
        file_path=file_path,
        file_type=file_type,
        raw_text=raw_text,
        **analysis,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return _to_response(resume)


@router.get("/history", response_model=list[ResumeListItem])
def get_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )
    return [
        ResumeListItem(
            id=r.id,
            file_name=r.file_name,
            ats_score=r.ats_score,
            ai_summary=r.ai_summary,
            top_role=r.role_predictions[0]["role"] if r.role_predictions else None,
            career_readiness_score=r.career_readiness_score,
            created_at=r.created_at,
        )
        for r in resumes
    ]


@router.get("/{resume_id}", response_model=AnalysisResponse)
def get_analysis(
    resume_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id, Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return _to_response(resume)


@router.post("/qa")
def resume_qa(
    request: QARequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resume = db.query(Resume).filter(
        Resume.id == request.resume_id, Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    context = build_resume_context(
        resume.parsed_data or {}, resume.ats_score or 0, resume.ats_breakdown
    )
    answer = answer_resume_qa(request.question, context)
    return {"question": request.question, "answer": answer}


@router.post("/cover-letter")
def create_cover_letter(
    request: CoverLetterRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resume = db.query(Resume).filter(
        Resume.id == request.resume_id, Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    role = request.target_role or (
        resume.role_predictions[0]["role"] if resume.role_predictions else "Software Engineer"
    )
    letter = generate_cover_letter(resume.parsed_data or {}, role)
    return {"target_role": role, "cover_letter": letter}


@router.post("/{resume_id}/download-cover-letter")
def download_cover_letter(
    resume_id: int,
    request: CoverLetterRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id, Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    role = request.target_role or (
        resume.role_predictions[0]["role"] if resume.role_predictions else "Software Engineer"
    )
    letter = generate_cover_letter(resume.parsed_data or {}, role)
    buffer = generate_cover_letter_pdf(letter, role)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=cover_letter_{resume_id}.pdf"},
    )


@router.get("/{resume_id}/interview-coach")
def get_interview_coach(
    resume_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Get comprehensive interview preparation roadmap."""
    from app.services.interview_coach_service import generate_complete_interview_roadmap
    
    resume = _get_resume(resume_id, current_user, db)
    experience_years = len(resume.parsed_data.get("experience", [])) * 1.5
    roadmap = generate_complete_interview_roadmap(resume.parsed_data or {}, experience_years)
    return roadmap


@router.get("/{resume_id}/interview-coach/project-questions/{project_index}")
def get_project_questions(
    resume_id: int,
    project_index: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Get detailed interview questions for a specific project."""
    from app.services.interview_coach_service import generate_project_questions
    
    resume = _get_resume(resume_id, current_user, db)
    projects = resume.parsed_data.get("projects", [])
    
    if project_index >= len(projects):
        raise HTTPException(status_code=404, detail="Project not found")
    
    questions = generate_project_questions(projects[project_index])
    return {
        "project_name": projects[project_index].get("name", f"Project {project_index + 1}"),
        "questions_by_category": questions,
    }


@router.get("/{resume_id}/interview-coach/dsa-roadmap")
def get_dsa_roadmap(
    resume_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Get DSA preparation roadmap."""
    from app.services.interview_coach_service import generate_dsa_roadmap, generate_preparation_plan
    
    resume = _get_resume(resume_id, current_user, db)
    experience_years = len(resume.parsed_data.get("experience", [])) * 1.5
    difficulty = "beginner" if experience_years < 1 else ("intermediate" if experience_years < 3 else "advanced")
    
    dsa = generate_dsa_roadmap(experience_years)
    plan_30 = generate_preparation_plan(30, difficulty)
    plan_60 = generate_preparation_plan(60, difficulty)
    
    return {
        "dsa_roadmap": dsa,
        "preparation_plan_30_days": plan_30,
        "preparation_plan_60_days": plan_60,
    }


@router.get("/{resume_id}/interview-coach/company-prep/{company_type}")
def get_company_prep(
    resume_id: int,
    company_type: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Get company-specific interview preparation."""
    from app.services.interview_coach_service import generate_company_prep
    
    resume = _get_resume(resume_id, current_user, db)
    prep = generate_company_prep(company_type)
    return prep


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id, Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    db.delete(resume)
    db.commit()


@router.get("/{resume_id}/download-pdf")
def download_pdf_report(
    resume_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resume = _get_resume(resume_id, current_user, db)
    buffer = generate_analysis_pdf(resume)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=analysis_report_{resume_id}.pdf"},
    )


@router.post("/compare")
def compare_resumes(
    request: CompareRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resumes = db.query(Resume).filter(
        Resume.id.in_(request.resume_ids),
        Resume.user_id == current_user.id,
    ).all()
    if len(resumes) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 resumes")

    return {
        "resumes": [
            {
                "id": r.id,
                "file_name": r.file_name,
                "ats_score": r.ats_score,
                "career_readiness": r.career_readiness_score,
                "template_rating": r.template_evaluation.get("rating") if r.template_evaluation else 0,
                "top_role": r.role_predictions[0]["role"] if r.role_predictions else None,
                "created_at": r.created_at.isoformat(),
            }
            for r in resumes
        ]
    }


def _get_resume(resume_id: int, user: User, db: Session) -> Resume:
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume
