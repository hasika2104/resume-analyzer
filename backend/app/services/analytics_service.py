"""Analytics and scoring metrics for the dashboard."""

INDUSTRY_BENCHMARKS = {
    "ats_score": 72,
    "resume_health": 70,
    "career_readiness": 65,
    "skill_strength": 68,
}


def compute_analytics(
    parsed: dict,
    ats_score: float,
    ats_breakdown: dict,
    skill_analysis: dict,
    role_predictions: list,
    job_recommendations: list,
    template_rating: float,
) -> dict:
    skill_strength = skill_analysis.get("skill_strength_score", 0)
    top_match = role_predictions[0]["confidence"] if role_predictions else 0
    job_match = job_recommendations[0]["match_percentage"] if job_recommendations else top_match

    career_readiness = round(
        ats_score * 0.35 + skill_strength * 0.25 + top_match * 0.25 + template_rating * 10 * 0.15,
        1,
    )
    resume_health = round(
        (ats_score + skill_strength + template_rating * 10) / 3,
        1,
    )

    skill_distribution = {
        "technical": len(skill_analysis.get("technical_skills", [])),
        "soft": len(skill_analysis.get("soft_skills", [])),
        "total": len(skill_analysis.get("all_skills", [])),
    }

    return {
        "ats_score": ats_score,
        "resume_health_score": resume_health,
        "career_readiness_score": career_readiness,
        "job_match_percentage": round(job_match, 1),
        "skill_distribution": skill_distribution,
        "industry_benchmark": {
            "your_ats": ats_score,
            "industry_avg_ats": INDUSTRY_BENCHMARKS["ats_score"],
            "your_health": resume_health,
            "industry_avg_health": INDUSTRY_BENCHMARKS["resume_health"],
            "your_readiness": career_readiness,
            "industry_avg_readiness": INDUSTRY_BENCHMARKS["career_readiness"],
            "percentile": _estimate_percentile(ats_score),
        },
        "top_role": role_predictions[0]["role"] if role_predictions else None,
        "top_role_confidence": role_predictions[0]["confidence"] if role_predictions else 0,
    }


def _estimate_percentile(ats_score: float) -> int:
    if ats_score >= 90:
        return 95
    if ats_score >= 80:
        return 85
    if ats_score >= 70:
        return 70
    if ats_score >= 60:
        return 50
    return 30


def get_admin_stats(db) -> dict:
    from app.models.user import User
    from app.models.resume import Resume
    from sqlalchemy import func

    total_users = db.query(User).count()
    total_resumes = db.query(Resume).count()
    avg_ats = db.query(func.avg(Resume.ats_score)).scalar() or 0

    role_counts: dict[str, int] = {}
    resumes = db.query(Resume).filter(Resume.role_predictions.isnot(None)).all()
    for r in resumes:
        if r.role_predictions:
            role = r.role_predictions[0].get("role", "Unknown")
            role_counts[role] = role_counts.get(role, 0) + 1

    recent = (
        db.query(Resume)
        .order_by(Resume.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "average_ats_score": round(float(avg_ats), 1),
        "role_distribution": role_counts,
        "recent_uploads": [
            {
                "id": r.id,
                "file_name": r.file_name,
                "ats_score": r.ats_score,
                "user_id": r.user_id,
                "created_at": r.created_at.isoformat(),
            }
            for r in recent
        ],
    }
