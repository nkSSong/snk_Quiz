from fastapi import FastAPI
from app.quiz.interface.router import router as quiz_router

app = FastAPI(title="SNK Quiz API")

app.include_router(quiz_router, prefix="/quiz", tags=["quiz"])