import re
from pathlib import Path

import pdfplumber
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    text_parts = []

    # pdfplumber — better layout preservation
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception:
        pass

    if text_parts:
        return "\n".join(text_parts)

    # Fallback to PyPDF2
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text_from_resume(file_path: str, file_type: str) -> str:
    path = Path(file_path)
    if file_type == "pdf" or path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    if file_type == "docx" or path.suffix.lower() == ".docx":
        return extract_text_from_docx(file_path)
    raise ValueError(f"Unsupported file type: {file_type}")


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()
