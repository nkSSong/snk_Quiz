from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_quizzes():
    return {"message": "퀴즈 목록"}