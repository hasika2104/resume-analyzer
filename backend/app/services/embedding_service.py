from functools import lru_cache

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def get_embedding_model():
    try:
        from sentence_transformers import SentenceTransformer
        from app.config import get_settings

        settings = get_settings()
        return SentenceTransformer(settings.EMBEDDING_MODEL)
    except Exception:
        return None


def generate_embedding(text: str) -> list[float]:
    model = get_embedding_model()
    if model is None or not text.strip():
        return _fallback_embedding(text)

    embedding = model.encode(text[:8000], convert_to_numpy=True)
    return embedding.tolist()


def _fallback_embedding(text: str) -> list[float]:
    """Simple hash-based fallback when sentence-transformers is unavailable."""
    np.random.seed(abs(hash(text[:500])) % (2**32))
    vec = np.random.randn(384)
    vec = vec / np.linalg.norm(vec)
    return vec.tolist()


def compute_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    if not embedding1 or not embedding2:
        return 0.0
    vec1 = np.array(embedding1).reshape(1, -1)
    vec2 = np.array(embedding2).reshape(1, -1)
    similarity = cosine_similarity(vec1, vec2)[0][0]
    return float(max(0, min(1, similarity)))


def build_resume_text(parsed_data: dict) -> str:
    parts = [
        parsed_data.get("name", ""),
        parsed_data.get("summary", ""),
        " ".join(parsed_data.get("skills", [])),
    ]
    for exp in parsed_data.get("experience", []):
        parts.append(f"{exp.get('title', '')} {exp.get('description', '')}")
    for proj in parsed_data.get("projects", []):
        parts.append(f"{proj.get('name', '')} {proj.get('description', '')}")
    for edu in parsed_data.get("education", []):
        parts.append(edu.get("degree", ""))
    return " ".join(parts)


def build_job_text(job) -> str:
    parts = [
        job.title,
        job.description,
        " ".join(job.required_skills or []),
        " ".join(job.preferred_technologies or []),
        " ".join(job.education_requirements or []),
    ]
    return " ".join(parts)
