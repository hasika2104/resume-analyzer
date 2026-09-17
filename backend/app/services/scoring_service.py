SKILL_RECOMMENDATIONS = {
    "python": ["FastAPI", "Django", "Flask"],
    "javascript": ["TypeScript", "React", "Node.js"],
    "react": ["Next.js", "Redux", "TypeScript"],
    "java": ["Spring Boot", "Microservices", "Kafka"],
    "machine learning": ["Deep Learning", "MLOps", "TensorFlow"],
    "aws": ["Terraform", "Kubernetes", "Docker"],
    "docker": ["Kubernetes", "CI/CD", "Helm"],
    "sql": ["PostgreSQL", "Data Modeling", "Query Optimization"],
}


def normalize_skill(skill: str) -> str:
    return skill.lower().strip()


def analyze_skill_gap(candidate_skills: list[str], required_skills: list[str]) -> dict:
    candidate_normalized = {normalize_skill(s): s for s in candidate_skills}
    required_normalized = {normalize_skill(s): s for s in required_skills}

    matching = []
    missing = []
    recommended = set()

    for req_norm, req_orig in required_normalized.items():
        matched = False
        for cand_norm, cand_orig in candidate_normalized.items():
            if req_norm in cand_norm or cand_norm in req_norm:
                matching.append(cand_orig)
                matched = True
                break
        if not matched:
            missing.append(req_orig)
            for key, recs in SKILL_RECOMMENDATIONS.items():
                if key in req_norm:
                    recommended.update(recs)

    for cand_norm in candidate_normalized:
        for key, recs in SKILL_RECOMMENDATIONS.items():
            if key in cand_norm:
                for rec in recs:
                    if normalize_skill(rec) not in candidate_normalized:
                        recommended.add(rec)

    recommended = [r for r in recommended if normalize_skill(r) not in candidate_normalized]

    return {
        "matching_skills": list(dict.fromkeys(matching)),
        "missing_skills": missing,
        "recommended_skills": recommended[:10],
    }


def compute_skill_score(matching: list[str], required: list[str]) -> float:
    if not required:
        return 8.0
    ratio = len(matching) / len(required)
    return round(min(10, ratio * 10), 2)


def compute_experience_score(years: float, min_exp: float, max_exp: float) -> float:
    if years is None:
        return 3.0
    if min_exp <= years <= max_exp:
        return 10.0
    if years < min_exp:
        gap = min_exp - years
        return round(max(0, 10 - gap * 2), 2)
    excess = years - max_exp
    return round(max(5, 10 - excess * 0.5), 2)


def compute_education_score(candidate_education: list, required_education: list) -> float:
    if not required_education:
        return 7.0
    if not candidate_education:
        return 2.0

    candidate_text = " ".join(
        f"{e.get('degree', '')} {e.get('institution', '')}".lower()
        for e in candidate_education
    )
    matches = sum(1 for req in required_education if req.lower() in candidate_text)
    ratio = matches / len(required_education)
    return round(min(10, 3 + ratio * 7), 2)


def compute_certification_score(certifications: list, required_skills: list) -> float:
    if not certifications:
        return 3.0
    cert_text = " ".join(certifications).lower()
    if not required_skills:
        return min(10, 5 + len(certifications))

    relevant = sum(1 for skill in required_skills if skill.lower() in cert_text)
    base = min(10, 4 + len(certifications) * 1.5)
    bonus = (relevant / max(len(required_skills), 1)) * 3
    return round(min(10, base + bonus), 2)


def compute_project_score(projects: list, required_skills: list, preferred_tech: list) -> float:
    if not projects:
        return 2.0

    all_keywords = [s.lower() for s in (required_skills or []) + (preferred_tech or [])]
    project_text = " ".join(
        f"{p.get('name', '')} {p.get('description', '')}".lower() for p in projects
    )

    if not all_keywords:
        desc_lengths = [len(p.get("description", "")) for p in projects]
        avg_len = sum(desc_lengths) / len(desc_lengths) if desc_lengths else 0
        return round(min(10, 4 + avg_len / 50 + len(projects)), 2)

    matches = sum(1 for kw in all_keywords if kw in project_text)
    ratio = matches / len(all_keywords)
    desc_bonus = min(3, sum(len(p.get("description", "")) for p in projects) / 200)
    return round(min(10, ratio * 7 + desc_bonus + min(2, len(projects) * 0.5)), 2)


def compute_final_score(
    skill_score: float,
    experience_score: float,
    education_score: float,
    certification_score: float,
    project_score: float,
    semantic_similarity: float = 0.0,
) -> dict:
    weighted = (
        skill_score * 0.40
        + experience_score * 0.25
        + education_score * 0.15
        + certification_score * 0.10
        + project_score * 0.10
    )
    semantic_boost = semantic_similarity * 0.5
    final = round(min(10, weighted + semantic_boost), 2)
    match_percentage = round(final * 10, 1)

    return {
        "final_score": final,
        "match_percentage": match_percentage,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "certification_score": certification_score,
        "project_score": project_score,
    }
