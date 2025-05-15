from pydantic import BaseModel, Field
from typing import List, Optional

class OptionCreate(BaseModel):
    text: str
    is_correct: bool

class QuestionCreate(BaseModel):
    text: str
    options: List[OptionCreate]

class QuizCreateRequest(BaseModel):
    title: str
    question_count: int
    is_question_order_random: bool = False
    is_option_order_random: bool = False
    questions: List[QuestionCreate]

class QuizListResponse(BaseModel):
    id: int
    title: str
    question_count: int

class QuizDetailOption(BaseModel):
    id: int
    text: str

class QuizDetailQuestion(BaseModel):
    id: int
    text: str
    options: List[QuizDetailOption]

class QuizDetailResponse(BaseModel):
    id: int
    title: str
    questions: List[QuizDetailQuestion]

class QuizSubmitAnswer(BaseModel):
    question_id: int
    selected_option_id: int

class QuizSubmitRequest(BaseModel):
    answers: List[QuizSubmitAnswer]

class QuizSubmitResult(BaseModel):
    score: int
    correct_count: int
    total: int
