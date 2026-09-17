"""AI Career Chat Assistant — rule-based career guidance."""

CAREER_RESPONSES = {
    "salary": (
        "Salary ranges vary by role, location, and experience. Based on industry data: "
        "Data Analyst ($65K–$110K), Software Engineer ($90K–$150K), Data Scientist ($100K–$160K). "
        "Use Glassdoor and Levels.fyi for location-specific data."
    ),
    "skills": (
        "Focus on building a T-shaped skill profile: deep expertise in 2-3 core skills plus "
        "breadth across related technologies. For tech roles, prioritize SQL, Python, and one "
        "visualization tool. Practice on Kaggle, LeetCode, and build portfolio projects."
    ),
    "interview": (
        "Prepare in three areas: (1) Technical — coding, SQL, or ML concepts depending on role. "
        "(2) Behavioral — use STAR method for situational questions. "
        "(3) Role-specific — research the company and prepare thoughtful questions."
    ),
    "roadmap": (
        "A typical career roadmap: (1) Assess current skills vs target role requirements. "
        "(2) Close top 3 skill gaps with courses and projects. (3) Build a portfolio on GitHub. "
        "(4) Network on LinkedIn. (5) Apply strategically to 10-15 roles per week."
    ),
    "resume": (
        "Resume tips: Keep it 1-2 pages, use action verbs, quantify achievements, "
        "tailor keywords to each job description, and include a professional summary. "
        "Upload your resume here for a detailed ATS analysis!"
    ),
}


def generate_chat_response(message: str, resume_context: dict | None = None) -> str:
    msg_lower = message.lower()

    for keyword, response in CAREER_RESPONSES.items():
        if keyword in msg_lower:
            base = response
            break
    else:
        if any(w in msg_lower for w in ["hello", "hi", "hey"]):
            base = (
                "Hello! I'm your AI Career Assistant. I can help with resume tips, "
                "skill development, interview prep, salary insights, and career roadmaps. "
                "What would you like to know?"
            )
        elif any(w in msg_lower for w in ["data", "analyst", "scientist", "engineer", "developer"]):
            base = (
                "Based on current market trends, tech and data roles are in high demand. "
                "Upload your resume for personalized role predictions and a learning roadmap. "
                "I can also suggest skills to develop for your target role."
            )
        elif any(w in msg_lower for w in ["learn", "course", "study", "certification"]):
            base = CAREER_RESPONSES["roadmap"]
        else:
            base = (
                "I'm here to help with your career journey! You can ask me about:\n"
                "• Resume improvement tips\n"
                "• Skill development strategies\n"
                "• Interview preparation\n"
                "• Salary expectations\n"
                "• Career roadmaps\n\n"
                "Upload a resume for personalized recommendations!"
            )

    if resume_context:
        ats = resume_context.get("ats_score")
        roles = resume_context.get("top_roles", [])
        if ats and roles:
            base += f"\n\nBased on your latest resume (ATS: {ats}/100), top roles: {', '.join(roles)}."

    return base
