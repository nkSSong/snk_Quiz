from fastapi import FastAPI
from app.quiz.interface.router import router as quiz_router
from app.seed import run_seed

app = FastAPI(title="SNK Quiz API")

@app.on_event("startup")
def startup_event():
    run_seed()

app.include_router(quiz_router, prefix="/quiz", tags=["quiz"])