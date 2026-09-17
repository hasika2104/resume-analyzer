"""Resume template evaluation and recommendation engine."""

RESUME_TEMPLATES = {
    "Modern ATS Professional": {
        "audience": ["Software Engineer", "Data Analyst", "Data Scientist", "AI Engineer", "Fresher"],
        "benefits": ["ATS Friendly", "Recruiter Friendly", "Clean Layout", "Better Readability"],
        "preview_style": "single-column",
        "description": "Clean single-column layout optimized for ATS parsing with clear section headers.",
    },
    "Minimal Tech Resume": {
        "audience": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Fresher"],
        "benefits": ["ATS Friendly", "Developer Focused", "Skills Highlight", "GitHub Ready"],
        "preview_style": "minimal",
        "description": "Minimal design highlighting technical skills and project links.",
    },
    "Data Professional": {
        "audience": ["Data Analyst", "Data Scientist", "Business Analyst", "AI Engineer"],
        "benefits": ["Skills Matrix", "Project Showcase", "ATS Optimized", "Analytics Focus"],
        "preview_style": "structured",
        "description": "Structured template emphasizing data skills, tools, and project outcomes.",
    },
    "Executive Career": {
        "audience": ["Product Manager", "Business Analyst"],
        "benefits": ["Leadership Focus", "Achievement Driven", "Professional Layout", "Impact Metrics"],
        "preview_style": "executive",
        "description": "Professional template for leadership and business roles with impact metrics.",
    },
    "Fresh Graduate": {
        "audience": ["Fresher"],
        "benefits": ["Education First", "Project Focus", "Internship Ready", "ATS Friendly"],
        "preview_style": "fresh",
        "description": "Education and projects focused template for entry-level candidates.",
    },
    "Creative Professional": {
        "audience": ["Product Manager"],
        "benefits": ["Visual Hierarchy", "Portfolio Links", "Modern Design", "Readable"],
        "preview_style": "modern",
        "description": "Modern design balancing visual appeal with ATS compatibility.",
    },
}


def evaluate_template(raw_text: str, file_path: str | None = None, file_type: str = "pdf") -> dict:
    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    problems = []
    score = 10.0

    avg_line_len = sum(len(l) for l in lines) / max(len(lines), 1)
    if avg_line_len > 100:
        problems.append("Dense text blocks reduce readability")
        score -= 1.0

    long_paragraphs = sum(1 for l in lines if len(l) > 150)
    if long_paragraphs > 3:
        problems.append("Large paragraphs — use bullet points instead")
        score -= 0.8

    if file_path and file_type == "pdf":
        layout_issues = _analyze_pdf_layout(file_path)
        problems.extend(layout_issues["problems"])
        score -= layout_issues["penalty"]

    word_count = len(raw_text.split())
    if word_count > 1200:
        problems.append("Resume may be too long — aim for 1-2 pages")
        score -= 0.5
    if word_count < 200:
        problems.append("Resume appears too short — add more detail")
        score -= 1.0

    section_count = sum(1 for kw in ["experience", "education", "skills", "projects"] if kw in raw_text.lower())
    if section_count < 3:
        problems.append("Missing standard section organization")
        score -= 0.7

    if "table" in raw_text.lower() or "|" in raw_text:
        problems.append("Complex tables may break ATS parsing")
        score -= 1.2

    multi_column = _detect_multi_column(raw_text)
    if multi_column:
        problems.append("Two-column layout detected — ATS may misread content order")
        score -= 1.5

    if not problems:
        problems.append("Consider adding more white space between sections")

    return {
        "rating": round(max(1, min(10, score)), 1),
        "problems": problems[:6],
        "ats_friendly": score >= 7,
        "readability_score": round(max(0, min(100, score * 10)), 1),
    }


def _analyze_pdf_layout(file_path: str) -> dict:
    problems = []
    penalty = 0.0
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages[:2]:
                chars = page.chars
                if not chars:
                    continue
                x_positions = [c["x0"] for c in chars]
                if len(set(round(x, 0) for x in x_positions)) > 8:
                    mid = page.width / 2
                    left = sum(1 for x in x_positions if x < mid)
                    right = sum(1 for x in x_positions if x >= mid)
                    if left > 20 and right > 20:
                        problems.append("Multiple columns detected in PDF layout")
                        penalty += 1.5
    except Exception:
        pass
    return {"problems": problems, "penalty": penalty}


def _detect_multi_column(text: str) -> bool:
    lines = text.split("\n")[:30]
    short_pairs = sum(1 for i in range(len(lines) - 1) if len(lines[i]) < 40 and len(lines[i + 1]) < 40)
    return short_pairs > 8


def recommend_templates(parsed: dict, role_predictions: list) -> list[dict]:
    top_role = role_predictions[0]["role"] if role_predictions else "Software Engineer"
    exp_years = len(parsed.get("experience", []))
    is_fresher = exp_years == 0 and len(parsed.get("education", [])) > 0
    
    skills = parsed.get("skills", [])
    is_data_role = any(role in top_role for role in ["Data", "Analyst", "AI"])
    has_projects = len(parsed.get("projects", [])) > 0

    audience = "Fresher" if is_fresher else top_role
    recommendations = []
    scores = {}

    # Score each template based on profile match
    for name, template in RESUME_TEMPLATES.items():
        score = 0
        
        # Audience match (primary criteria)
        if audience in template["audience"] or top_role in template["audience"]:
            score += 40
        
        # Role-specific scoring
        if is_fresher and "Fresher" in template["audience"]:
            score += 20
        if is_data_role and "Data" in template["audience"]:
            score += 20
        if not is_fresher and "Full Stack" in top_role and "Full Stack" in template["audience"]:
            score += 15
        if has_projects and ("Projects" in name or "Tech" in name):
            score += 10
            
        # Benefits alignment
        ats_heavy = any(b == "ATS Friendly" for b in template["benefits"])
        if ats_heavy:
            score += 5
            
        scores[name] = score

    # Sort by score and return top 3
    sorted_templates = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    for idx, (name, score) in enumerate(sorted_templates[:3]):
        template = RESUME_TEMPLATES[name]
        recommendations.append({
            "name": name,
            "description": template["description"],
            "benefits": template["benefits"],
            "preview_style": template["preview_style"],
            "why_recommended": _generate_recommendation_reason(name, audience, top_role, is_fresher, is_data_role, has_projects),
            "match_score": int((score / 100) * 100) if score > 0 else 50,
        })

    if not recommendations:
        recommendations.append({
            "name": "Modern ATS Professional",
            "description": RESUME_TEMPLATES["Modern ATS Professional"]["description"],
            "benefits": RESUME_TEMPLATES["Modern ATS Professional"]["benefits"],
            "preview_style": "single-column",
            "why_recommended": "Universal ATS-friendly template suitable for most roles.",
            "match_score": 85,
        })

    return recommendations[:3]


def _generate_recommendation_reason(name: str, audience: str, top_role: str, is_fresher: bool, is_data_role: bool, has_projects: bool) -> str:
    reasons = []
    
    if "Fresher" in name:
        reasons.append("Perfect for entry-level candidates")
        reasons.append("emphasizes education and projects")
    elif "Data" in name and is_data_role:
        reasons.append(f"Tailored for {top_role} roles")
        reasons.append("highlights analytical skills")
    elif "Tech" in name or "Minimal" in name:
        reasons.append("Developer-focused layout")
        reasons.append("GitHub integration ready")
    elif "Executive" in name:
        reasons.append("Professional and leadership-oriented")
        reasons.append("metrics-driven presentation")
    else:
        reasons.append(f"Optimized for {audience}")
        reasons.append("ATS-optimized single-column layout")
    
    if has_projects:
        reasons.append("great for showcasing projects")
    
    reason_text = f"{reasons[0]}. {reasons[1]}"
    if len(reasons) > 2:
        reason_text += f" and {reasons[2]}"
    reason_text += "."
    
    return reason_text.replace("  ", " ")
