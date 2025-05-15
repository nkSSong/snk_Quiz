from sqlalchemy.orm import Session
from app.quiz.domain.models import Quiz, Question, Option, QuizResult, Answer
from app.quiz.application.dto import QuizCreateRequest, QuizUpdateRequest, QuizSubmitRequest, QuizSubmitResult
from fastapi import HTTPException
import random
from datetime import datetime

quiz_sessions_cache = {}  # Global cache to persist quiz sessions per user-quiz across requests

class QuizService:
    def __init__(self, db: Session):
        self.db = db
        # In-memory cache for quiz sessions: {f"{user_id}:{quiz_id}": [(question, [options...]), ...]}
        self.quiz_sessions = {}

    def create_quiz(self, data: QuizCreateRequest):
        if not data.questions:
            raise HTTPException(status_code=400, detail="At least one question required")
        quiz = Quiz(
            title=data.title,
            question_count=data.question_count,
            is_question_order_random=data.is_question_order_random,
            is_option_order_random=data.is_option_order_random
        )
        self.db.add(quiz)
        self.db.flush()

        for q in data.questions:
            if len(q.options) < 3:
                raise HTTPException(status_code=400, detail="Each question must have at least 3 options")
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


    def get_detail(self, quiz_id: int, page: int = 1, per_page: int = 10, user_id: int = None):
        quiz = self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        session_key = f"{user_id}:{quiz_id}"
        if session_key not in quiz_sessions_cache or not quiz_sessions_cache[session_key]:
            all_questions = quiz.questions
            if len(all_questions) < quiz.question_count:
                raise HTTPException(status_code=400, detail="Not enough questions to meet the configured count")
            selected_questions = random.sample(all_questions, quiz.question_count)

            # Shuffle options if required
            final_questions = []
            for q in selected_questions:
                options = q.options[:]
                if quiz.is_option_order_random:
                    options = random.sample(options, len(options))
                final_questions.append((q, options))

            quiz_sessions_cache[session_key] = final_questions

        final_questions = quiz_sessions_cache[session_key]

        start = (page - 1) * per_page
        end = start + per_page
        paginated = final_questions[start:end]

        return {
            "id": quiz.id,
            "title": quiz.title,
            "questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "options": [{"id": o.id, "text": o.text} for o in options]
                } for q, options in paginated
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

        # Remove cached quiz session after submission
        session_key = f"{user_id}:{quiz_id}"
        if session_key in quiz_sessions_cache:
            del quiz_sessions_cache[session_key]

        return QuizSubmitResult(score=score, correct_count=correct_count, total=len(data.answers))

    def update_quiz(self, quiz_id: int, data: QuizUpdateRequest):
        quiz = self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        quiz.title = data.title
        quiz.question_count = data.question_count,
        quiz.is_question_order_random = data.is_question_order_random
        quiz.is_option_order_random = data.is_option_order_random

        with self.db.no_autoflush:
            # Delete existing questions and options
            for question in quiz.questions:
                for option in question.options:
                    self.db.delete(option)
                self.db.delete(question)

        self.db.flush()

        # Add updated questions and options
        for q in data.questions:
            if len(q.options) < 3:
                raise HTTPException(status_code=400, detail="Each question must have at least 3 options")
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
        return {
            "message": "Quiz updated",
            "quiz_id": quiz.id,
            "title": quiz.title,
            "question_count": quiz.question_count
        }
    def get_all_with_status(self, page: int, per_page: int, user):
        quizzes = self.db.query(Quiz).offset((page - 1) * per_page).limit(per_page).all()

        if user.is_admin:
            return [
                {
                    "id": q.id,
                    "title": q.title,
                    "question_count": q.question_count
                } for q in quizzes
            ]

        submitted_quiz_ids = {
            result.quiz_id for result in self.db.query(QuizResult).filter(QuizResult.user_id == user.id).all()
        }

        return [
            {
                "id": q.id,
                "title": q.title,
                "question_count": q.question_count,
                "status": "submitted" if q.id in submitted_quiz_ids else "pending"
            } for q in quizzes
        ]