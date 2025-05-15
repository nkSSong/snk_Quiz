from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.quiz.application.service import QuizService
from app.quiz.application.dto import (
    QuizCreateRequest,
    QuizDetailResponse,
    QuizSubmitRequest,
    QuizSubmitResult,
)
from app.user.domain.models import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/quizzes", tags=["Quiz"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz_data: QuizCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can create quizzes")
    return QuizService(db).create_quiz(quiz_data)

@router.get("/", response_model=List[dict])
def list_quizzes(db: Session = Depends(get_db)):
    return QuizService(db).get_all()

@router.get("/{quiz_id}", response_model=QuizDetailResponse)
def get_quiz_detail(
    quiz_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    return QuizService(db).get_detail(quiz_id, page, per_page)

@router.post("/{quiz_id}/submit", response_model=QuizSubmitResult)
def submit_quiz(
    quiz_id: int,
    data: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return QuizService(db).submit(quiz_id, user_id=current_user.id, data=data)

@router.delete("/{quiz_id}")
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can delete quizzes")
    return QuizService(db).delete_quiz(quiz_id)
