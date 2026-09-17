"""Career role prediction, job recommendations, skill gap, and learning roadmap."""

ROLE_PROFILES = {
    "Software Engineer": {
        "skills": ["python", "java", "javascript", "algorithms", "git", "sql", "oop", "data structures"],
        "salary": "$90,000 – $150,000",
        "path": "Junior Dev → Software Engineer → Senior Engineer → Tech Lead",
    },
    "Data Analyst": {
        "skills": ["sql", "excel", "python", "tableau", "power bi", "statistics", "data analysis", "visualization"],
        "salary": "$65,000 – $110,000",
        "path": "Analyst → Senior Analyst → Analytics Manager → Director of Analytics",
    },
    "Data Scientist": {
        "skills": ["python", "machine learning", "statistics", "sql", "pandas", "numpy", "deep learning", "tensorflow"],
        "salary": "$100,000 – $160,000",
        "path": "Data Analyst → Data Scientist → Senior DS → ML Engineer / Lead",
    },
    "AI Engineer": {
        "skills": ["python", "deep learning", "nlp", "tensorflow", "pytorch", "machine learning", "transformers"],
        "salary": "$120,000 – $180,000",
        "path": "ML Engineer → AI Engineer → Senior AI Engineer → AI Architect",
    },
    "Full Stack Developer": {
        "skills": ["javascript", "react", "node.js", "html", "css", "sql", "rest api", "mongodb"],
        "salary": "$85,000 – $140,000",
        "path": "Junior Full Stack → Developer → Senior → Engineering Manager",
    },
    "Frontend Developer": {
        "skills": ["javascript", "react", "html", "css", "typescript", "vue", "angular", "tailwind"],
        "salary": "$75,000 – $130,000",
        "path": "Junior Frontend → Developer → Senior Frontend → UI Architect",
    },
    "Backend Developer": {
        "skills": ["python", "java", "sql", "rest api", "docker", "microservices", "postgresql", "redis"],
        "salary": "$85,000 – $145,000",
        "path": "Junior Backend → Developer → Senior Backend → Platform Architect",
    },
    "Business Analyst": {
        "skills": ["sql", "excel", "requirements", "stakeholder", "documentation", "agile", "power bi", "analysis"],
        "salary": "$70,000 – $115,000",
        "path": "Junior BA → Business Analyst → Senior BA → Product Manager",
    },
    "Product Manager": {
        "skills": ["product", "agile", "stakeholder", "roadmap", "analytics", "user research", "sql", "strategy"],
        "salary": "$110,000 – $170,000",
        "path": "Associate PM → Product Manager → Senior PM → Director of Product",
    },
    "DevOps Engineer": {
        "skills": ["docker", "kubernetes", "aws", "ci/cd", "linux", "terraform", "jenkins", "git"],
        "salary": "$100,000 – $155,000",
        "path": "SysAdmin → DevOps Engineer → Senior DevOps → Platform Engineer",
    },
}

ROLE_LEARNING_PATHS = {
    "Data Scientist": [
        ("Learn Statistics", "Master probability, hypothesis testing, and statistical modeling", ["Khan Academy Statistics", "Coursera Statistics"]),
        ("Learn Machine Learning", "Study supervised/unsupervised learning algorithms", ["Andrew Ng ML Course", "Scikit-learn docs"]),
        ("Build 3 Projects", "Create end-to-end ML projects with real datasets", ["Kaggle", "GitHub portfolio"]),
        ("Learn Deep Learning", "Study neural networks and deep learning frameworks", ["Fast.ai", "Deep Learning Specialization"]),
        ("Practice Interview Questions", "Prepare ML system design and coding questions", ["LeetCode", "ML Interview Questions"]),
    ],
    "Data Analyst": [
        ("Master SQL", "Advanced queries, joins, window functions", ["SQLBolt", "Mode Analytics SQL"]),
        ("Learn Python for Analysis", "Pandas, NumPy, data cleaning", ["DataCamp", "Kaggle Learn"]),
        ("Data Visualization", "Tableau or Power BI dashboards", ["Tableau Public", "Microsoft Learn"]),
        ("Statistics Fundamentals", "Descriptive and inferential statistics", ["Khan Academy", "Coursera"]),
        ("Build Portfolio Projects", "3 analysis projects with storytelling", ["Kaggle Datasets", "GitHub"]),
    ],
    "Software Engineer": [
        ("Data Structures & Algorithms", "Master core CS fundamentals", ["LeetCode", "Cracking the Coding Interview"]),
        ("System Design", "Learn scalable architecture patterns", ["System Design Primer", "Grokking SD"]),
        ("Build Projects", "Full-stack or backend projects on GitHub", ["Build your own X", "GitHub"]),
        ("Open Source Contributions", "Contribute to real-world projects", ["GitHub Explore", "First Timers Only"]),
        ("Interview Preparation", "Coding + behavioral interviews", ["LeetCode", "Pramp"]),
    ],
}

DEFAULT_ROADMAP = [
    ("Identify Target Role", "Research job requirements and industry trends", ["LinkedIn Jobs", "Glassdoor"]),
    ("Close Skill Gaps", "Focus on top 3 missing skills for your target role", ["Coursera", "Udemy"]),
    ("Build Portfolio", "Create 2-3 projects demonstrating your skills", ["GitHub", "Personal website"]),
    ("Network & Apply", "Connect with professionals and apply strategically", ["LinkedIn", "Indeed"]),
    ("Interview Prep", "Practice technical and behavioral questions", ["LeetCode", "Pramp"]),
]


def predict_roles(parsed: dict) -> list[dict]:
    skills_lower = {s.lower() for s in parsed.get("skills", [])}
    text_lower = " ".join(parsed.get("skills", [])).lower()
    experience_text = " ".join(
        f"{e.get('title', '')} {e.get('description', '')}" for e in parsed.get("experience", [])
    ).lower()
    combined = text_lower + " " + experience_text

    predictions = []
    for role, profile in ROLE_PROFILES.items():
        role_skills = profile["skills"]
        matches = sum(1 for s in role_skills if s in skills_lower or s in combined)
        confidence = round(min(98, (matches / len(role_skills)) * 100 + len(skills_lower) * 0.5), 1)
        if confidence >= 30:
            predictions.append({"role": role, "confidence": confidence})

    predictions.sort(key=lambda x: x["confidence"], reverse=True)
    return predictions[:5] if predictions else [{"role": "Software Engineer", "confidence": 45.0}]


def generate_job_recommendations(role_predictions: list[dict], parsed: dict) -> list[dict]:
    skills_lower = {s.lower() for s in parsed.get("skills", [])}
    recommendations = []

    for pred in role_predictions[:3]:
        role = pred["role"]
        profile = ROLE_PROFILES.get(role, {})
        role_skills = profile.get("skills", [])
        missing = [s.title() for s in role_skills if s not in skills_lower][:5]

        recommendations.append({
            "title": role,
            "match_percentage": pred["confidence"],
            "missing_skills": missing,
            "salary_range": profile.get("salary", "$60,000 – $120,000"),
            "career_path": profile.get("path", "Entry Level → Mid Level → Senior → Lead"),
        })

    return recommendations


def analyze_skill_gap(parsed: dict, target_role: str) -> dict:
    skills_lower = {s.lower() for s in parsed.get("skills", [])}
    profile = ROLE_PROFILES.get(target_role, ROLE_PROFILES["Software Engineer"])
    required = profile["skills"]

    matching = [s.title() for s in required if s in skills_lower]
    missing = [s.title() for s in required if s not in skills_lower]

    return {
        "current_skills": parsed.get("skills", []),
        "target_role": target_role,
        "missing_skills": missing,
        "matching_skills": matching,
    }


def generate_learning_roadmap(target_role: str, skill_gap: dict, experience_years: float = 0, parsed: dict | None = None) -> list[dict]:
    """Generate personalized learning roadmap based on current skills, gaps, and experience."""
    steps = ROLE_LEARNING_PATHS.get(target_role, DEFAULT_ROADMAP)
    roadmap = []
    missing = skill_gap.get("missing_skills", [])
    current_skills = skill_gap.get("current_skills", [])
    matching = skill_gap.get("matching_skills", [])
    
    # Calculate learning pace based on experience
    if experience_years < 1:
        pace = "intensive"
        weeks_per_step = 12
    elif experience_years < 3:
        pace = "accelerated"
        weeks_per_step = 8
    else:
        pace = "standard"
        weeks_per_step = 6
    
    # Prioritize missing skills
    priority_missing = sorted(missing, key=lambda x: x.lower() in " ".join(s.lower() for s in current_skills))
    
    # Create personalized roadmap
    for i, (title, description, resources) in enumerate(steps, 1):
        month_label = f"Month {i}"
        custom_description = description
        
        # Customize first step with focus on top missing skills
        if i == 1 and missing:
            top_skills = ", ".join(missing[:2])
            custom_description = f"{description} Your priority: master {top_skills}."
        
        # Customize for experience level
        if i == 2:
            if experience_years < 1:
                custom_description = description + " Start with fundamentals and best practices."
            elif experience_years >= 5:
                custom_description = description + " Focus on advanced patterns and optimization."
        
        # Tailor resources based on experience
        custom_resources = resources
        if experience_years >= 5 and i >= 3:
            custom_resources = resources + ["Advanced documentation", "Research papers"]
        
        roadmap.append({
            "step": i,
            "month": month_label,
            "title": title,
            "description": custom_description,
            "resources": custom_resources,
            "difficulty": "Beginner" if i <= 2 else ("Intermediate" if i <= 4 else "Advanced"),
            "estimated_weeks": weeks_per_step,
        })
    
    return roadmap


def generate_improvements(parsed: dict, ats_breakdown: dict) -> list[str]:
    tips = []
    sections = parsed.get("sections", {})

    if not sections.get("summary"):
        tips.append("Add a professional summary at the top of your resume.")
    if not sections.get("skills"):
        tips.append("Include a dedicated skills section with technical and soft skills.")
    if not sections.get("certifications") and not parsed.get("certifications"):
        tips.append("Add a certifications section to strengthen credibility.")
    if ats_breakdown.get("contact", 100) < 80:
        tips.append("Ensure your contact information (email, phone) is clearly visible.")
    if ats_breakdown.get("keywords", 100) < 70:
        tips.append("Include more industry-relevant keywords (e.g., Agile, KPI, automation).")
    if not parsed.get("has_measurable_achievements"):
        tips.append("Quantify project impact with numbers (e.g., 'Increased efficiency by 30%').")

    weak_projects = [p for p in parsed.get("projects", []) if len(p.get("description", "")) < 30]
    if weak_projects:
        tips.append(f"Expand descriptions for {len(weak_projects)} project(s) with technologies and outcomes.")

    if ats_breakdown.get("experience", 100) < 70:
        tips.append("Add more detail to work experience with action verbs and measurable results.")

    if ats_breakdown.get("formatting", 100) < 70:
        tips.append("Improve formatting: use consistent bullet points and clear section headers.")

    word_count = parsed.get("word_count", 0)
    if word_count < 250:
        tips.append("Resume appears too short — add more detail to experience and projects.")
    elif word_count > 1500:
        tips.append("Resume may be too long — aim for 1-2 pages with concise bullet points.")

    missing_tech = []
    for role_skill in ["sql", "python", "excel"]:
        if role_skill not in {s.lower() for s in parsed.get("skills", [])}:
            if role_skill == "sql":
                missing_tech.append("SQL")
            elif role_skill == "python":
                missing_tech.append("Python")
    if missing_tech:
        tips.append(f"Consider adding keywords: {', '.join(missing_tech)}.")

    return tips[:8]


def generate_ai_summary(parsed: dict, role_predictions: list[dict], ats_score: float) -> str:
    name = parsed.get("name", "The candidate")
    skills = parsed.get("skills", [])[:5]
    top_roles = [r["role"] for r in role_predictions[:2]]
    exp_count = len(parsed.get("experience", []))
    proj_count = len(parsed.get("projects", []))

    skills_text = ", ".join(skills) if skills else "various technical skills"
    roles_text = " and ".join(top_roles) if top_roles else "multiple roles"

    summary = (
        f"{name} has an ATS score of {ats_score}/100. "
        f"Strong skills in {skills_text}"
    )
    if exp_count:
        summary += f" with {exp_count} work experience entries"
    if proj_count:
        summary += f" and {proj_count} project(s)"
    summary += f". Best suited for {roles_text} roles."

    return summary


def generate_skill_analysis(parsed: dict) -> dict:
    technical = parsed.get("technical_skills", [])
    soft = parsed.get("soft_skills", [])
    all_skills = parsed.get("skills", [])

    strength = min(100, len(all_skills) * 6 + len(technical) * 4 + len(soft) * 3)
    if parsed.get("sections", {}).get("skills"):
        strength = min(100, strength + 10)

    return {
        "all_skills": all_skills,
        "technical_skills": technical,
        "soft_skills": soft,
        "skill_strength_score": round(strength, 1),
    }


def generate_interview_questions(skills: list[str], parsed: dict | None = None, experience_years: float = 0) -> dict:
    """Generate interview questions tailored to candidate's skills and experience level."""
    
    # Determine experience level
    if experience_years == 0 and parsed:
        exp = parsed.get("experience", [])
        experience_years = len(exp) * 1.5
    
    is_junior = experience_years < 2
    is_mid = 2 <= experience_years < 5
    is_senior = experience_years >= 5
    
    # Build tech stack from skills
    skills_lower = [s.lower() for s in skills] if skills else []
    has_python = any("python" in s for s in skills_lower)
    has_java = any("java" in s for s in skills_lower)
    has_js = any("javascript" in s or "react" in s or "node" in s for s in skills_lower)
    has_sql = any("sql" in s or "database" in s for s in skills_lower)
    has_ml = any("machine" in s or "ml" in s or "deep" in s for s in skills_lower)
    has_devops = any("docker" in s or "kubernetes" in s or "aws" in s for s in skills_lower)
    
    # Experience-level appropriate technical questions
    if is_junior:
        technical_easy = [
            "Explain the difference between a list and a dictionary/map.",
            "What is the purpose of version control and Git workflows?",
            "What is an API and how does REST architecture work?",
        ]
        technical_medium = [
            "Describe the concept of object-oriented programming and inheritance.",
            "How do you approach debugging a complex issue in your code?",
            "Explain the difference between synchronous and asynchronous programming.",
        ]
        technical_hard = [
            "Design a simple system architecture for a scalable web application.",
            "How would you optimize code performance for a bottleneck you discovered?",
            "Explain a complex system you built and the architectural decisions you made.",
        ]
    elif is_mid:
        technical_easy = [
            "Design a solution to handle 1 million daily active users.",
            "Explain microservices architecture vs monolithic design.",
            "How do you approach system design interviews?",
        ]
        technical_medium = [
            "Design a scalable database schema for a complex business problem.",
            "Explain how you would implement caching strategies in production.",
            "How do you ensure code quality and maintainability in a large team?",
        ]
        technical_hard = [
            "Design a distributed system handling failures and consistency.",
            "How would you architect a real-time analytics platform?",
            "Explain trade-offs in choosing between different database technologies.",
        ]
    else:
        technical_easy = [
            "How do you mentor junior engineers and build high-performing teams?",
            "Describe your approach to technical debt management and refactoring.",
            "How do you lead architectural decisions in complex systems?",
        ]
        technical_medium = [
            "Design a global-scale system with sub-100ms latency requirements.",
            "How would you approach building a data platform for ML systems?",
            "Explain your strategy for system resilience and disaster recovery.",
        ]
        technical_hard = [
            "Design a highly distributed system handling petabyte-scale data.",
            "How would you architect a system supporting multiple business models?",
            "Explain complex tradeoffs in building cutting-edge infrastructure.",
        ]
    
    # Tech-specific questions
    tech_specific = []
    if has_python:
        tech_specific.append("Describe your experience with Python and discuss a complex project where you optimized performance.")
    if has_js:
        tech_specific.append("Explain your experience with JavaScript/React and how you handle state management in large applications.")
    if has_sql:
        tech_specific.append("Describe complex SQL queries you've written and how you optimize database performance.")
    if has_ml:
        tech_specific.append("Walk through your experience with machine learning - model selection, training, and deployment.")
    if has_devops:
        tech_specific.append("Describe your DevOps experience - CI/CD pipelines, containerization, and infrastructure as code.")
    if has_java:
        tech_specific.append("Explain your Java experience and how you handle concurrent programming and memory management.")
    
    # Fill remaining slots with skill-specific questions
    for skill in skills[:3]:
        if len(tech_specific) < 5:
            tech_specific.append(f"Describe your most impactful project using {skill} and what you learned.")
    
    # Behavioral questions
    behavioral = [
        "Tell me about yourself, your career journey, and what drives your technical growth.",
        "Describe a challenging project you led and how you handled setbacks or conflicts.",
        "Give an example of when you had to learn something new quickly to solve a problem.",
        "How do you approach code reviews and handling criticism from peers?",
        "Tell me about a time you had to make a difficult decision between technical debt and features.",
    ]
    
    return {
        "technical": {"easy": technical_easy, "medium": technical_medium, "hard": technical_hard},
        "behavioral": behavioral[:3],
        "skill_specific": tech_specific[:5],
    }
