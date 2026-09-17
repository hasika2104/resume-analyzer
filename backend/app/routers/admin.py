from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.schemas.auth import UserResponse
from app.services.analytics_service import get_admin_stats
from app.utils.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/stats")
def admin_stats(
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    return get_admin_stats(db)


@router.get("/users", response_model=list[UserResponse])
def list_users(
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.get("/resumes")
def list_all_resumes(
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    resumes = db.query(Resume).order_by(Resume.created_at.desc()).limit(100).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "file_name": r.file_name,
            "ats_score": r.ats_score,
            "career_readiness_score": r.career_readiness_score,
            "top_role": r.role_predictions[0]["role"] if r.role_predictions else None,
            "created_at": r.created_at.isoformat(),
        }
        for r in resumes
    ]
