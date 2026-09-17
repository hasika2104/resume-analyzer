TECHNICAL_QUESTIONS = {
    "easy": [
        "Explain the difference between a list and a tuple in Python.",
        "What is the purpose of version control systems like Git?",
        "Describe what REST API stands for and its key principles.",
        "What is the difference between SQL and NoSQL databases?",
        "Explain what a variable is and how scope works in programming.",
    ],
    "medium": [
        "How would you optimize a slow database query?",
        "Explain the concept of dependency injection and its benefits.",
        "Describe how you would design a caching strategy for a web application.",
        "What are microservices and what are their trade-offs?",
        "Explain how authentication differs from authorization.",
    ],
    "hard": [
        "Design a scalable system to handle 1 million concurrent users.",
        "Explain CAP theorem and how it applies to distributed systems.",
        "How would you implement a rate limiter for an API?",
        "Describe strategies for handling eventual consistency in distributed databases.",
        "Walk through how you would debug a memory leak in a production application.",
    ],
}

HR_QUESTIONS = [
    "Tell me about yourself and your career journey.",
    "Why are you interested in this role and our company?",
    "Describe a challenging situation at work and how you handled it.",
    "Where do you see yourself in 5 years?",
    "How do you handle tight deadlines and competing priorities?",
    "Describe a time you worked effectively in a team.",
    "What motivates you in your professional life?",
    "How do you stay updated with industry trends?",
]

PROJECT_QUESTIONS = [
    "Walk me through your most significant project and your specific contributions.",
    "What technical challenges did you face in your projects and how did you overcome them?",
    "How did you measure the success of your project?",
    "If you could rebuild one of your projects, what would you do differently?",
    "Describe a project where you had to learn a new technology quickly.",
]


def generate_ai_feedback(
    parsed_data: dict,
    skill_gap: dict,
    scores: dict,
) -> dict:
    tips = []
    missing = skill_gap.get("missing_skills", [])
    projects = parsed_data.get("projects", [])
    certifications = parsed_data.get("certifications", [])

    if missing:
        tips.append(f"Add proficiency in: {', '.join(missing[:5])} to strengthen your profile.")

    weak_projects = [p for p in projects if len(p.get("description", "")) < 30]
    if weak_projects:
        tips.append(
            f"Expand descriptions for {len(weak_projects)} project(s) with technologies used and measurable outcomes."
        )

    if not certifications:
        tips.append("Consider obtaining industry certifications relevant to your target role.")

    if scores.get("experience_score", 0) < 5:
        tips.append("Highlight quantifiable achievements and impact in your work experience section.")

    if scores.get("education_score", 0) < 5:
        tips.append("Ensure your education section clearly lists degrees, institutions, and graduation dates.")

    if len(parsed_data.get("skills", [])) < 5:
        tips.append("Include a dedicated skills section with both technical and soft skills.")

    cert_recommendations = []
    for skill in missing[:3]:
        cert_recommendations.append(f"Consider certification in {skill}")

    return {
        "missing_skills": missing,
        "improvement_tips": tips,
        "certification_recommendations": cert_recommendations,
        "weak_projects": [p.get("name", "Unnamed") for p in weak_projects],
        "overall_assessment": _overall_assessment(scores.get("final_score", 0)),
    }


def _overall_assessment(score: float) -> str:
    if score >= 8:
        return "Strong candidate profile with excellent alignment to job requirements."
    if score >= 6:
        return "Good candidate with solid fundamentals. Some skill gaps can be addressed."
    if score >= 4:
        return "Moderate fit. Candidate may need additional training in key areas."
    return "Limited alignment with job requirements. Consider for junior or alternate roles."


def generate_interview_questions(skills: list[str]) -> dict:
    skill_specific = []
    for skill in skills[:5]:
        skill_specific.extend([
            f"Explain your experience with {skill} and a project where you used it.",
            f"What are the best practices when working with {skill}?",
            f"Compare {skill} with alternative technologies you have used.",
        ])

    return {
        "technical": {
            "easy": TECHNICAL_QUESTIONS["easy"][:3],
            "medium": TECHNICAL_QUESTIONS["medium"][:3],
            "hard": TECHNICAL_QUESTIONS["hard"][:3],
        },
        "hr": HR_QUESTIONS[:5],
        "project_based": PROJECT_QUESTIONS[:3],
        "skill_specific": skill_specific[:10],
    }
