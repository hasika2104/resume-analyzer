import re
from functools import lru_cache

TECH_SKILLS = {
    "python", "java", "javascript", "typescript", "react", "angular", "vue", "node.js",
    "nodejs", "django", "flask", "fastapi", "spring", "sql", "postgresql", "mysql",
    "mongodb", "redis", "docker", "kubernetes", "aws", "azure", "gcp", "terraform",
    "git", "linux", "c++", "c#", "go", "golang", "rust", "html", "css", "tailwind",
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "nlp", "spark", "tableau", "power bi", "excel", "r", "matlab",
    "next.js", "express", "graphql", "rest api", "microservices", "devops", "ci/cd",
    "selenium", "pytest", "figma", "jira", "snowflake", "databricks", "airflow",
    "statistics", "data analysis", "data visualization", "etl", "dbt", "kafka",
}

SOFT_SKILLS = {
    "communication", "leadership", "teamwork", "problem solving", "critical thinking",
    "time management", "adaptability", "collaboration", "creativity", "analytical",
    "interpersonal", "presentation", "negotiation", "conflict resolution", "mentoring",
    "project management", "attention to detail", "work ethic", "flexibility",
}

INDUSTRY_KEYWORDS = {
    "agile", "scrum", "stakeholder", "cross-functional", "deliverables", "kpi",
    "roi", "optimization", "automation", "scalable", "architecture", "deployment",
    "implementation", "analysis", "strategy", "research", "development", "design",
    "testing", "documentation", "requirements", "solutions", "performance", "metrics",
    "insights", "dashboard", "reporting", "forecasting", "modeling", "pipeline",
}


@lru_cache(maxsize=1)
def get_nlp():
    try:
        import spacy
        from app.config import get_settings
        return spacy.load(get_settings().SPACY_MODEL)
    except OSError:
        return None


@lru_cache(maxsize=1)
def _init_nltk():
    try:
        import nltk
        for resource in ("punkt", "punkt_tab", "stopwords"):
            try:
                nltk.data.find(f"tokenizers/{resource}" if "punkt" in resource else f"corpora/{resource}")
            except LookupError:
                nltk.download(resource, quiet=True)
        return True
    except Exception:
        return False


def extract_email(text: str) -> str | None:
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    patterns = [
        r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        r"\b\d{10}\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not lines:
        return "Unknown"

    nlp = get_nlp()
    if nlp:
        doc = nlp(lines[0][:100])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()

    first = lines[0]
    if len(first) < 50 and not extract_email(first) and not re.search(r"\d{3}", first):
        return first
    return "Unknown"


def extract_skills(text: str) -> dict:
    text_lower = text.lower()
    technical = set()
    soft = set()

    for skill in TECH_SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
            technical.add(skill.title() if skill.islower() else skill)

    for skill in SOFT_SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
            soft.add(skill.title())

    return {
        "all": sorted(technical | soft),
        "technical": sorted(technical),
        "soft": sorted(soft),
    }


def extract_education(text: str) -> list[dict]:
    education = []
    degree_patterns = [
        r"(B\.?S\.?|B\.?A\.?|B\.?Tech|M\.?S\.?|M\.?A\.?|M\.?Tech|Ph\.?D\.?|MBA|Bachelor|Master|Doctor)"
    ]
    lines = text.split("\n")
    in_section = False

    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        if any(kw in line_lower for kw in ["education", "academic", "qualification"]):
            in_section = True
            continue
        if in_section and any(kw in line_lower for kw in ["experience", "work", "skills", "projects"]):
            break
        if in_section and line.strip():
            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    education.append({
                        "degree": line.strip(),
                        "institution": lines[i + 1].strip() if i + 1 < len(lines) else "",
                    })

    if not education:
        for line in lines:
            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    education.append({"degree": line.strip(), "institution": ""})

    return education[:5]


def extract_experience(text: str) -> list[dict]:
    experience = []
    lines = text.split("\n")
    in_section = False
    current: dict | None = None
    date_pattern = r"(\d{4}|\w+\s+\d{4})\s*[-–—]\s*(\d{4}|present|current|\w+\s+\d{4})"

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        if any(kw in line_lower for kw in ["experience", "employment", "work history"]):
            in_section = True
            continue
        if in_section and any(kw in line_lower for kw in ["education", "skills", "projects", "certification"]):
            break

        if in_section and line_stripped:
            date_match = re.search(date_pattern, line_stripped, re.IGNORECASE)
            if date_match or (len(line_stripped) < 80 and not line_stripped.startswith("-")):
                if current:
                    experience.append(current)
                current = {
                    "title": line_stripped,
                    "company": "",
                    "duration": date_match.group(0) if date_match else "",
                    "description": "",
                }
            elif current and line_stripped.startswith("-"):
                current["description"] += line_stripped + " "

    if current:
        experience.append(current)
    return experience[:10]


def extract_projects(text: str) -> list[dict]:
    projects = []
    lines = text.split("\n")
    in_section = False

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        if any(kw in line_lower for kw in ["projects", "portfolio"]):
            in_section = True
            continue
        if in_section and any(kw in line_lower for kw in ["certification", "skills", "education"]):
            break
        if in_section and line_stripped:
            if line_stripped.startswith(("-", "•")):
                projects.append({"name": line_stripped.lstrip("-• ").strip(), "description": ""})
            elif projects and not projects[-1]["description"]:
                projects[-1]["description"] = line_stripped

    return projects[:10]


def extract_certifications(text: str) -> list[str]:
    certs = []
    keywords = ["certified", "certification", "certificate", "aws certified", "google cloud"]
    for line in text.split("\n"):
        line_stripped = line.strip()
        if any(kw in line_stripped.lower() for kw in keywords) and len(line_stripped) < 150:
            certs.append(line_stripped)
    return certs[:10]


def extract_keywords(text: str) -> list[str]:
    text_lower = text.lower()
    found = [kw.title() for kw in INDUSTRY_KEYWORDS if kw in text_lower]

    if _init_nltk():
        try:
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            tokens = word_tokenize(text_lower)
            stops = set(stopwords.words("english"))
            freq: dict[str, int] = {}
            for t in tokens:
                if t.isalpha() and len(t) > 3 and t not in stops:
                    freq[t] = freq.get(t, 0) + 1
            top = sorted(freq, key=freq.get, reverse=True)[:15]
            found.extend(w.title() for w in top if w.title() not in found)
        except Exception:
            pass

    return found[:20]


def has_measurable_achievements(text: str) -> bool:
    patterns = [
        r"\d+%", r"\$\d+", r"\d+\+?\s*(years|months|users|clients|projects)",
        r"increased|decreased|improved|reduced|saved|generated|achieved",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def extract_links(text: str) -> dict:
    links = {}
    linkedin = re.search(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+/?", text, re.I)
    if linkedin:
        links["linkedin"] = linkedin.group(0)
    github = re.search(r"(?:https?://)?(?:www\.)?github\.com/[\w-]+/?", text, re.I)
    if github:
        links["github"] = github.group(0)
    portfolio = re.search(r"(?:https?://)?[\w.-]+\.(?:dev|io|me|com)/[\w./-]*", text, re.I)
    if portfolio and "linkedin" not in portfolio.group(0).lower() and "github" not in portfolio.group(0).lower():
        links["portfolio"] = portfolio.group(0)
    return links


def parse_resume(text: str) -> dict:
    cleaned = text.strip()
    skills = extract_skills(cleaned)
    experience = extract_experience(cleaned)
    education = extract_education(cleaned)
    projects = extract_projects(cleaned)
    certifications = extract_certifications(cleaned)
    keywords = extract_keywords(cleaned)
    links = extract_links(cleaned)
    sections = detect_sections(cleaned)

    return {
        "name": extract_name(cleaned),
        "email": extract_email(cleaned),
        "phone": extract_phone(cleaned),
        "links": links,
        "skills": skills["all"],
        "technical_skills": skills["technical"],
        "soft_skills": skills["soft"],
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "keywords": keywords,
        "sections": sections,
        "has_summary": sections.get("summary", False),
        "has_measurable_achievements": has_measurable_achievements(cleaned),
        "word_count": len(cleaned.split()),
    }


def detect_sections(text: str) -> dict:
    text_lower = text.lower()
    return {
        "summary": any(kw in text_lower for kw in ["summary", "objective", "profile", "about me"]),
        "skills": any(kw in text_lower for kw in ["skills", "technical skills", "core competencies"]),
        "experience": any(kw in text_lower for kw in ["experience", "employment", "work history"]),
        "education": any(kw in text_lower for kw in ["education", "academic", "qualification"]),
        "projects": any(kw in text_lower for kw in ["projects", "portfolio"]),
        "certifications": any(kw in text_lower for kw in ["certification", "certificates", "licenses"]),
    }
