# app/seed.py
from app.core.database import SessionLocal
from app.user.domain.models import User
from app.quiz.domain.models import Quiz, Question, Option
from sqlalchemy.exc import IntegrityError

def run_seed():
    db = SessionLocal()

    try:
        if db.query(User).count() == 0:
            admin = User(email="admin@example.com", password="hashed123", is_admin=True)
            db.add(admin)
            db.add_all([
                User(email="user1@example.com", password="userpass1", is_admin=False),
                User(email="user2@example.com", password="userpass2", is_admin=False),
                User(email="user3@example.com", password="userpass3", is_admin=False),
            ])

        if db.query(Quiz).count() == 0:
            quizzes = []
            question_counts = [3, 4, 3, 1, 3]  # 각 퀴즈별 문제 수

            for i in range(5):
                quiz = Quiz(
                    title=f"샘플 퀴즈 {i+1}",
                    question_count=question_counts[i],  # 👈 실제 질문 수로 지정
                    is_question_order_random=True,
                    is_option_order_random=True,
                )
                db.add(quiz)
                db.flush()
                quizzes.append(quiz)

                for qn in range(1, question_counts[i] + 1):
                    question = Question(quiz_id=quiz.id, text=f"퀴즈 {i+1} 질문 {qn}")
                    db.add(question)
                    db.flush()

                    db.add_all([
                        Option(question_id=question.id, text="선택지 A", is_correct=(qn % 3 == 0)),
                        Option(question_id=question.id, text="선택지 B", is_correct=(qn % 3 == 1)),
                        Option(question_id=question.id, text="선택지 C", is_correct=(qn % 3 == 2)),
                    ])

        db.commit()

    except IntegrityError:
        db.rollback()
    finally:
        db.close()