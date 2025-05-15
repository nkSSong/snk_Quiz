

from sqlalchemy.orm import Session
from app.quiz.domain.models import Quiz, Question, Option, QuizResult, Answer
from app.quiz.application.dto import QuizCreateRequest, QuizSubmitRequest, QuizSubmitResult
from fastapi import HTTPException
import random
from datetime import datetime

class QuizService:
    def __init__(self, db: Session):
        self.db = db

    def create_quiz(self, data: QuizCreateRequest):
        quiz = Quiz(
            title=data.title,
            question_count=data.question_count,
            is_question_order_random=data.is_question_order_random,
            is_option_order_random=data.is_option_order_random
        )
        self.db.add(quiz)
        self.db.flush()

        for q in data.questions:
            question = Question(quiz_id=quiz.id, text=q.text)
            self.db.add(question)
            self.db.flush()

            correct_count = 0
            for opt in q.options:
                option = Option(
                    question_id=question.id,
                    text=opt.text,
                    is_correct=opt.is_correct
                )
                if opt.is_correct:
                    correct_count += 1
                self.db.add(option)

            if correct_count != 1:
                raise HTTPException(status_code=400, detail="Each question must have exactly one correct answer")

        self.db.commit()
        return {"message": "Quiz created", "quiz_id": quiz.id}

    def get_all(self):
        quizzes = self.db.query(Quiz).all()
        return [
            {
                "id": q.id,
                "title": q.title,
                "question_count": q.question_count
            } for q in quizzes
        ]

    def get_detail(self, quiz_id: int, page: int = 1, per_page: int = 10):
        quiz = self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        questions = quiz.questions
        if quiz.is_question_order_random:
            questions = random.sample(questions, len(questions))

        start = (page - 1) * per_page
        end = start + per_page
        paginated = questions[start:end]

        return {
            "id": quiz.id,
            "title": quiz.title,
            "questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "options": random.sample([
                        {"id": o.id, "text": o.text} for o in q.options
                    ], len(q.options)) if quiz.is_option_order_random else [
                        {"id": o.id, "text": o.text} for o in q.options
                    ]
                } for q in paginated
            ]
        }

    def delete_quiz(self, quiz_id: int):
        quiz = self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        self.db.delete(quiz)
        self.db.commit()
        return {"message": "Quiz deleted"}

    def submit(self, quiz_id: int, user_id: int, data: QuizSubmitRequest):
        quiz = self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        score = 0
        correct_count = 0
        for answer in data.answers:
            opt = self.db.query(Option).filter(Option.id == answer.selected_option_id).first()
            if opt and opt.is_correct:
                score += 1
                correct_count += 1

        result = QuizResult(
            user_id=user_id,
            quiz_id=quiz_id,
            score=score,
            submitted_at=datetime.utcnow().isoformat()
        )
        self.db.add(result)
        self.db.flush()

        for a in data.answers:
            ans = Answer(
                result_id=result.id,
                question_id=a.question_id,
                selected_option_id=a.selected_option_id
            )
            self.db.add(ans)

        self.db.commit()

        return QuizSubmitResult(score=score, correct_count=correct_count, total=len(data.answers))