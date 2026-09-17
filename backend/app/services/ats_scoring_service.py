"""ATS scoring engine — 0–100 with user-facing breakdown categories."""


def compute_ats_score(parsed: dict, raw_text: str) -> dict:
    formatting = _score_formatting(parsed, raw_text)
    skills = _score_skills(parsed)
    experience = _score_experience(parsed)
    keywords = _score_keywords(parsed)
    projects = _score_projects(parsed)

    breakdown = {
        "formatting": formatting,
        "skills": skills,
        "experience": experience,
        "keywords": keywords,
        "projects": projects,
        "structure": _score_structure(parsed.get("sections", {})),
        "contact": _score_contact(parsed),
        "education": _score_education(parsed),
        "readability": _score_readability(parsed, raw_text),
        "ats_compatibility": _score_ats_compat(parsed, raw_text),
    }

    weights = {
        "formatting": 0.15,
        "skills": 0.20,
        "experience": 0.20,
        "keywords": 0.15,
        "projects": 0.15,
        "structure": 0.05,
        "contact": 0.05,
        "readability": 0.05,
    }

    total = round(sum(breakdown[k] * weights[k] for k in weights), 1)
    display_breakdown = {
        "formatting": breakdown["formatting"],
        "skills": breakdown["skills"],
        "experience": breakdown["experience"],
        "keywords": breakdown["keywords"],
        "projects": breakdown["projects"],
    }

    return {"ats_score": total, "ats_breakdown": display_breakdown, "full_breakdown": breakdown}


def _score_structure(sections: dict) -> float:
    required = ["skills", "experience", "education"]
    present = sum(1 for s in required if sections.get(s))
    return round(min(100, (present / len(required)) * 85 + 15), 1)


def _score_contact(parsed: dict) -> float:
    score = 0
    if parsed.get("name") and parsed["name"] != "Unknown":
        score += 30
    if parsed.get("email"):
        score += 35
    if parsed.get("phone"):
        score += 20
    links = parsed.get("links", {})
    if links.get("linkedin"):
        score += 8
    if links.get("github"):
        score += 7
    return round(min(100, score), 1)


def _score_skills(parsed: dict) -> float:
    skills = parsed.get("skills", [])
    if not skills:
        return 20.0
    return round(min(100, 40 + len(skills) * 5 + len(parsed.get("technical_skills", [])) * 3), 1)


def _score_experience(parsed: dict) -> float:
    experience = parsed.get("experience", [])
    if not experience:
        return 15.0
    score = min(50, len(experience) * 15)
    if parsed.get("has_measurable_achievements"):
        score += 30
    desc_avg = sum(len(e.get("description", "")) for e in experience) / len(experience)
    score += min(20, desc_avg / 8)
    return round(min(100, score), 1)


def _score_education(parsed: dict) -> float:
    education = parsed.get("education", [])
    return round(min(100, 40 + len(education) * 25), 1) if education else 25.0


def _score_keywords(parsed: dict) -> float:
    combined = len(set(parsed.get("keywords", []) + parsed.get("skills", [])))
    return round(min(100, 25 + combined * 4), 1)


def _score_projects(parsed: dict) -> float:
    projects = parsed.get("projects", [])
    if not projects:
        return 20.0
    desc_score = sum(len(p.get("description", "")) for p in projects) / len(projects)
    return round(min(100, 35 + len(projects) * 12 + desc_score / 5), 1)


def _score_formatting(parsed: dict, raw_text: str) -> float:
    word_count = parsed.get("word_count", len(raw_text.split()))
    score = 50.0
    if 300 <= word_count <= 1000:
        score += 30
    elif 200 <= word_count <= 1200:
        score += 15
    if parsed.get("has_summary"):
        score += 10
    if parsed.get("sections", {}).get("projects"):
        score += 10
    return round(min(100, score), 1)


def _score_readability(parsed: dict, raw_text: str) -> float:
    lines = [l for l in raw_text.split("\n") if l.strip()]
    avg_len = sum(len(l) for l in lines) / max(len(lines), 1)
    if avg_len < 80:
        return 85.0
    if avg_len < 120:
        return 70.0
    return 55.0


def _score_ats_compat(parsed: dict, raw_text: str) -> float:
    score = 80.0
    if "|" in raw_text or "table" in raw_text.lower():
        score -= 15
    if len(raw_text.split()) > 1500:
        score -= 10
    return round(max(0, score), 1)
