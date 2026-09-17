from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.chat import ChatMessage
from app.schemas.analysis import ChatRequest, ChatMessageResponse
from app.services.openai_service import chat_with_context, build_resume_context, is_openai_available
from app.services.chat_service import generate_chat_response
from app.utils.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["Career Copilot"])


@router.post("/", response_model=ChatMessageResponse)
def send_message(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resume_context = ""
    if request.resume_id:
        resume = db.query(Resume).filter(
            Resume.id == request.resume_id, Resume.user_id == current_user.id
        ).first()
        if resume:
            resume_context = build_resume_context(
                resume.parsed_data or {}, resume.ats_score or 0, resume.ats_breakdown
            )

    history_msgs = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
        .all()[::-1]
    )
    history = [{"role": m.role, "content": m.content} for m in history_msgs]

    user_msg = ChatMessage(user_id=current_user.id, role="user", content=request.message)
    db.add(user_msg)
    db.flush()

    if is_openai_available() and resume_context:
        response_text = chat_with_context(request.message, resume_context, history)
    elif is_openai_available():
        response_text = chat_with_context(request.message, "{}", history)
    else:
        ctx = {}
        if request.resume_id and resume_context:
            import json
            ctx = json.loads(resume_context)
        response_text = generate_chat_response(request.message, {
            "ats_score": ctx.get("ats_score"),
            "top_roles": [],
        })

    assistant_msg = ChatMessage(user_id=current_user.id, role="assistant", content=response_text)
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)
    return assistant_msg


@router.get("/history", response_model=list[ChatMessageResponse])
def get_chat_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    limit: int = 50,
):
    msgs = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )
    return msgs[::-1]


@router.get("/status")
def chat_status():
    return {"openai_enabled": is_openai_available()}
