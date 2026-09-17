import json
from typing import Any

from app.config import get_settings

settings = get_settings()


def is_openai_available() -> bool:
    return bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip())


def _get_client():
    if not is_openai_available():
        return None
    from openai import OpenAI
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def build_resume_context(parsed: dict, ats_score: float = 0, ats_breakdown: dict | None = None) -> str:
    ctx = {
        "name": parsed.get("name"),
        "email": parsed.get("email"),
        "phone": parsed.get("phone"),
        "links": parsed.get("links", {}),
        "skills": parsed.get("skills", []),
        "technical_skills": parsed.get("technical_skills", []),
        "education": parsed.get("education", []),
        "experience": parsed.get("experience", []),
        "projects": parsed.get("projects", []),
        "certifications": parsed.get("certifications", []),
        "ats_score": ats_score,
        "ats_breakdown": ats_breakdown or {},
    }
    return json.dumps(ctx, indent=2)


def chat_with_context(
    message: str,
    resume_context: str,
    history: list[dict] | None = None,
) -> str:
    client = _get_client()
    if not client:
        from app.services.chat_service import generate_chat_response
        ctx = json.loads(resume_context) if resume_context else {}
        return generate_chat_response(message, {
            "ats_score": ctx.get("ats_score"),
            "top_roles": [],
        })

    system_prompt = """You are Career Copilot, an expert AI career coach and resume advisor.
You have access to the user's resume data. Provide personalized, actionable advice.
Be concise, professional, and encouraging. Use bullet points when listing multiple items.
You can help with: resume improvements, ATS optimization, job eligibility, skill development,
interview prep, cover letters, certifications, salary expectations, and career paths."""

    messages = [{"role": "system", "content": f"{system_prompt}\n\nResume Context:\n{resume_context}"}]
    for msg in (history or [])[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1200,
        )
        return response.choices[0].message.content or ""
    except Exception:
        from app.services.chat_service import generate_chat_response
        ctx = json.loads(resume_context) if resume_context else {}
        return generate_chat_response(message, {
            "ats_score": ctx.get("ats_score"),
            "top_roles": [],
        })


def answer_resume_qa(question: str, resume_context: str) -> str:
    return chat_with_context(question, resume_context)


def generate_ai_summary_gpt(parsed: dict, role_predictions: list) -> str:
    client = _get_client()
    if not client:
        from app.services.career_service import generate_ai_summary
        return generate_ai_summary(parsed, role_predictions, 0)

    roles = ", ".join(r["role"] for r in role_predictions[:3])
    prompt = f"""Write a 2-3 sentence recruiter-friendly resume summary for this candidate.
Mention key skills, experience highlights, and suitable roles ({roles}).

Resume data:
{json.dumps(parsed, indent=2)[:3000]}"""

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=200,
        )
        return response.choices[0].message.content or ""
    except Exception:
        from app.services.career_service import generate_ai_summary
        return generate_ai_summary(parsed, role_predictions, 0)


def generate_improvements_gpt(parsed: dict, ats_breakdown: dict) -> list[str]:
    client = _get_client()
    if not client:
        from app.services.career_service import generate_improvements
        return generate_improvements(parsed, ats_breakdown)

    prompt = f"""Analyze this resume and provide exactly 6 actionable improvement suggestions.
Focus on: missing sections, weak descriptions, missing keywords, formatting, measurable achievements.

ATS Breakdown: {json.dumps(ats_breakdown)}
Resume: {json.dumps(parsed, indent=2)[:2500]}

Return ONLY a JSON array of strings, no other text."""

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=600,
        )
        text = response.choices[0].message.content or "[]"
        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            return [line.strip("- •") for line in text.split("\n") if line.strip()][:6]
    except Exception:
        from app.services.career_service import generate_improvements
        return generate_improvements(parsed, ats_breakdown)


def rewrite_resume_sections(parsed: dict) -> list[dict]:
    client = _get_client()
    rewrites = []

    items_to_rewrite = []
    for exp in parsed.get("experience", [])[:3]:
        desc = exp.get("description", "") or exp.get("title", "")
        if desc and len(desc) > 10:
            items_to_rewrite.append(("experience", desc))
    for proj in parsed.get("projects", [])[:3]:
        desc = f"{proj.get('name', '')} {proj.get('description', '')}".strip()
        if desc and len(desc) > 10:
            items_to_rewrite.append(("project", desc))

    if not items_to_rewrite:
        items_to_rewrite = [("summary", "Professional seeking growth opportunities with relevant skills.")]

    if not client:
        for section_type, before in items_to_rewrite[:4]:
            after = _fallback_rewrite(before)
            rewrites.append({"section": section_type, "before": before, "after": after})
        return rewrites

    try:
        for section_type, before in items_to_rewrite[:4]:
            prompt = f"""Rewrite this resume {section_type} bullet to be ATS-optimized.
Use action verbs, quantify impact where possible, include relevant keywords.
Return ONLY the improved text, no explanation.

Before: {before}"""

            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=200,
            )
            after = response.choices[0].message.content or _fallback_rewrite(before)
            rewrites.append({"section": section_type, "before": before, "after": after.strip()})
    except Exception:
        for section_type, before in items_to_rewrite[:4]:
            after = _fallback_rewrite(before)
            rewrites.append({"section": section_type, "before": before, "after": after})

    return rewrites


def generate_interview_questions_gpt(parsed: dict, experience_years: float = 0) -> dict:
    client = _get_client()
    if not client:
        from app.services.career_service import generate_interview_questions
        return generate_interview_questions(parsed.get("skills", []), parsed, experience_years)

    # Build detailed context
    skills = ", ".join(parsed.get("skills", [])[:10]) or "various"
    experience = parsed.get("experience", [])
    titles = [e.get("title", "") for e in experience[:3]]
    projects = parsed.get("projects", [])
    project_names = [p.get("name", "") for p in projects[:2]]
    
    # Determine experience level
    if experience_years < 2:
        level = "junior/entry-level"
    elif experience_years < 5:
        level = "mid-level"
    else:
        level = "senior"
    
    context = f"Candidate Background:\n- Experience Level: {level} ({experience_years:.1f} years)\n- Skills: {skills}\n- Roles: {', '.join(titles)}\n- Projects: {', '.join(project_names)}" if project_names else f"Candidate Background:\n- Experience Level: {level} ({experience_years:.1f} years)\n- Skills: {skills}\n- Roles: {', '.join(titles)}"
    
    prompt = f"""Generate personalized interview questions for a candidate. {context}

Create questions tailored to their experience level and specific background. Include:
- 3 technical questions (easy, medium, hard - appropriate for their level)
- 3 behavioral questions about their background
- 2-3 questions specific to their projects and skills

Return ONLY valid JSON with this exact structure:
{{
  "technical": {{"easy": ["q1"], "medium": ["q2"], "hard": ["q3"]}},
  "behavioral": ["q1", "q2", "q3"],
  "skill_specific": ["q1", "q2"]
}}"""

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=900,
        )
        text = response.choices[0].message.content or "{}"
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            from app.services.career_service import generate_interview_questions
            return generate_interview_questions(parsed.get("skills", []), parsed, experience_years)
    except Exception:
        from app.services.career_service import generate_interview_questions
        return generate_interview_questions(parsed.get("skills", []), parsed, experience_years)


def _generate_structured_cover_letter(parsed: dict, target_role: str) -> str:
    """Generate a structured cover letter from resume data without AI"""
    from datetime import datetime
    
    name = parsed.get("name", "[Your Name]")
    email = parsed.get("email", "[Email Address]")
    phone = parsed.get("phone", "[Phone Number]")
    links = parsed.get("links", {})
    portfolio = links.get("github") or links.get("portfolio") or "[Portfolio/GitHub]"
    
    skills = parsed.get("skills", [])[:6]
    skills_str = ", ".join(skills) if skills else "professional skills"
    
    experience = parsed.get("experience", [])
    achievements = []
    for exp in experience[:2]:
        description = exp.get("description", "")
        if description:
            if isinstance(description, list):
                achievements.extend(description[:2])
            else:
                achievements.append(description)
    
    education = parsed.get("education", [])
    degree = education[0].get("degree", "") if education else ""
    school = education[0].get("school", "") if education else ""
    
    projects = parsed.get("projects", [])
    project_highlight = projects[0].get("name", "") if projects else ""
    
    current_date = datetime.now().strftime("%B %d, %Y")
    
    cover_letter = f"""{name}
{phone}
{email}
{portfolio}

{current_date}

[Hiring Manager's Name]
[Company Name]
[Company Address]
[City, State, ZIP Code]

Subject: Application for {target_role} Position

Dear [Hiring Manager's Name],

I am writing to express my strong interest in the {target_role} position at [Company Name]. With my background in {skills_str} and proven track record in delivering impactful solutions, I am confident I can contribute significantly to your team and help achieve your organization's goals.

In my professional experience, I have developed strong expertise in {skills_str}. My accomplishments include:
• {achievements[0] if achievements else "Delivered high-quality projects with attention to detail and technical excellence"}
• {achievements[1] if len(achievements) > 1 else "Collaborated with cross-functional teams to achieve business objectives"}{f"• Completed education in {degree} from {school}" if degree else ""}

What particularly excites me about this opportunity is the chance to leverage my {skills_str.split(',')[0]} skills to make a meaningful impact. My proven ability to [adapt/solve problems/innovate] positions me well to contribute immediately to your team's success.

I would welcome the opportunity to discuss how my qualifications and enthusiasm can benefit [Company Name]. Thank you for considering my application. I look forward to the possibility of speaking with you further.

Sincerely,

{name}"""
    
    return cover_letter


def generate_cover_letter(parsed: dict, target_role: str) -> str:
    client = _get_client()
    if not client:
        return _generate_structured_cover_letter(parsed, target_role)

    name = parsed.get("name", "candidate")
    skills = ", ".join(parsed.get("skills", [])[:5]) or "professional expertise"
    experience_summary = f"{len(parsed.get('experience', []))} years of professional experience"
    
    prompt = f"""Generate a professional cover letter for a {target_role} position using this resume data.

Candidate Name: {name}
Skills: {skills}
Background: {experience_summary}
Key Details: {json.dumps(parsed, indent=2)[:1500]}

Format the cover letter with:
1. Contact header: name, phone, email
2. Date
3. Employer section (with placeholders: [Hiring Manager's Name], [Company Name], [Company Address])
4. Subject line
5. Dear [Hiring Manager's Name],
6. Introduction paragraph - state the position and express interest
7. Body paragraph 1 - highlight relevant skills and qualifications matching the role
8. Body paragraph 2 - specific achievements and examples demonstrating value
9. Closing paragraph - reaffirm interest and thank them
10. Sincerely, [Name]

Make it professional, personalized to the candidate's background, and compelling. 3-4 paragraphs in body."""

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content or _generate_structured_cover_letter(parsed, target_role)
    except Exception:
        return _generate_structured_cover_letter(parsed, target_role)


def _fallback_rewrite(text: str) -> str:
    verbs = ["Developed", "Implemented", "Optimized", "Led", "Designed", "Delivered"]
    verb = verbs[len(text) % len(verbs)]
    return f"{verb} key initiatives leveraging modern technologies, achieving measurable improvements in efficiency and quality. {text[:80]}"
