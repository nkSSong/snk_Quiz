from fastapi import FastAPI, Depends
from app.quiz.interface.router import router as quiz_router
from app.seed import run_seed

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.user.domain.models import User


app = FastAPI(title="SNK Quiz API")

@app.on_event("startup")
def startup_event():
    run_seed()


app.include_router(quiz_router)
