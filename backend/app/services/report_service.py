from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def generate_analysis_pdf(resume) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=18, spaceAfter=16)
    heading = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=13, spaceAfter=8)
    body = styles["Normal"]
    elements = []

    elements.append(Paragraph("AI Resume Analysis Report", title_style))
    elements.append(Paragraph(f"File: {resume.file_name}", body))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"ATS Score: {resume.ats_score}/100", heading))
    elements.append(Paragraph(
        f"Resume Health: {resume.resume_health_score}/100 | "
        f"Career Readiness: {resume.career_readiness_score}/100",
        body,
    ))
    elements.append(Spacer(1, 10))

    if resume.ats_breakdown:
        rows = [["Category", "Score"]] + [
            [k.title(), f"{v}/100"] for k, v in resume.ats_breakdown.items()
        ]
        table = Table(rows, colWidths=[3 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6366f1")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 14))

    if resume.ai_summary:
        elements.append(Paragraph("AI Summary", heading))
        elements.append(Paragraph(resume.ai_summary, body))
        elements.append(Spacer(1, 10))

    if resume.improvements:
        elements.append(Paragraph("Improvements", heading))
        for tip in resume.improvements[:6]:
            elements.append(Paragraph(f"• {tip}", body))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_improved_resume_pdf(resume) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=22, spaceAfter=6)
    section = ParagraphStyle("Section", parent=styles["Heading2"], fontSize=13, spaceAfter=6, textColor=colors.HexColor("#6366f1"))
    body = styles["Normal"]
    elements = []

    parsed = resume.parsed_data or {}
    improved = resume.improved_content or {}
    template = improved.get("recommended_template", "Modern ATS Professional")

    elements.append(Paragraph(str(parsed.get("name", "Professional Resume")), title))
    contact_parts = [parsed.get("email"), parsed.get("phone")]
    links = parsed.get("links", {})
    contact_parts.extend(links.values())
    elements.append(Paragraph(" | ".join(p for p in contact_parts if p), body))
    elements.append(Paragraph(f"Template: {template}", body))
    elements.append(Spacer(1, 16))

    summary = improved.get("summary") or resume.ai_summary or ""
    if summary:
        elements.append(Paragraph("PROFESSIONAL SUMMARY", section))
        elements.append(Paragraph(summary, body))
        elements.append(Spacer(1, 12))

    skills = parsed.get("skills", [])
    if skills:
        elements.append(Paragraph("SKILLS", section))
        elements.append(Paragraph(", ".join(skills[:25]), body))
        elements.append(Spacer(1, 12))

    rewrites = resume.resume_rewrites or improved.get("rewrites", [])
    if rewrites:
        elements.append(Paragraph("EXPERIENCE & PROJECTS (AI-Optimized)", section))
        for rw in rewrites[:6]:
            elements.append(Paragraph(f"• {rw.get('after', rw.get('before', ''))}", body))
        elements.append(Spacer(1, 12))

    if parsed.get("education"):
        elements.append(Paragraph("EDUCATION", section))
        for edu in parsed["education"][:3]:
            elements.append(Paragraph(edu.get("degree", ""), body))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_cover_letter_pdf(cover_letter_text: str, target_role: str = "Professional") -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5 * inch, leftMargin=0.75 * inch, rightMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    
    # Define custom styles
    header_style = ParagraphStyle("Header", parent=styles["Normal"], fontSize=9, spaceAfter=1)
    date_style = ParagraphStyle("Date", parent=styles["Normal"], fontSize=11, spaceAfter=12)
    employer_style = ParagraphStyle("Employer", parent=styles["Normal"], fontSize=10, spaceAfter=1)
    subject_style = ParagraphStyle("Subject", parent=styles["Normal"], fontSize=10, fontName="Helvetica-Bold", spaceAfter=10)
    greeting_style = ParagraphStyle("Greeting", parent=styles["Normal"], fontSize=11, spaceAfter=8)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=11, spaceAfter=10, alignment=4)  # justified
    closing_style = ParagraphStyle("Closing", parent=styles["Normal"], fontSize=11, spaceAfter=20)
    signature_style = ParagraphStyle("Signature", parent=styles["Normal"], fontSize=11, spaceAfter=1)
    
    elements = []
    lines = cover_letter_text.strip().split('\n')
    
    i = 0
    # Parse header (contact info)
    while i < len(lines) and lines[i].strip() and '@' not in lines[i]:
        elements.append(Paragraph(lines[i].strip(), header_style))
        i += 1
    
    # Add spacing after header
    if i > 0:
        elements.append(Spacer(1, 12))
    
    # Parse date
    while i < len(lines) and lines[i].strip() and lines[i].strip()[0].isdigit():
        elements.append(Paragraph(lines[i].strip(), date_style))
        elements.append(Spacer(1, 6))
        i += 1
    
    elements.append(Spacer(1, 6))
    
    # Parse employer section (until Subject line)
    while i < len(lines) and not lines[i].strip().startswith("Subject:"):
        if lines[i].strip():
            elements.append(Paragraph(lines[i].strip(), employer_style))
        i += 1
    
    # Parse subject line
    while i < len(lines) and lines[i].strip().startswith("Subject:"):
        elements.append(Paragraph(lines[i].strip(), subject_style))
        elements.append(Spacer(1, 6))
        i += 1
    
    # Parse greeting
    while i < len(lines) and (lines[i].strip().startswith("Dear") or not lines[i].strip()):
        if lines[i].strip().startswith("Dear"):
            elements.append(Paragraph(lines[i].strip(), greeting_style))
        i += 1
    
    # Parse body content
    current_para = ""
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Sincerely,"):
            if current_para:
                elements.append(Paragraph(current_para, body_style))
                current_para = ""
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(line, closing_style))
            i += 1
            break
        elif line and line[0] == "•":
            # Bullet point - treat as part of paragraph
            current_para += f"<br/>{line}"
        elif not line:
            # Empty line - end of paragraph
            if current_para:
                elements.append(Paragraph(current_para, body_style))
                current_para = ""
        else:
            # Regular text
            current_para += " " + line if current_para else line
        i += 1
    
    # Add remaining signature
    while i < len(lines):
        if lines[i].strip():
            elements.append(Paragraph(lines[i].strip(), signature_style))
        i += 1
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
