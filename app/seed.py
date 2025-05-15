from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from app.user.domain.models import User
from app.quiz.domain.models import Quiz, Question, Option
from sqlalchemy.exc import IntegrityError

def run_seed(session: Session = None):
    db = session or SessionLocal()

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
            import random

            quizzes = []

            for i in range(22):
                if i == 0:
                    question_count = 11
                else:
                    question_count = random.randint(1, 4)

                quiz = Quiz(
                    title=f"샘플 퀴즈 {i+1}",
                    question_count=question_count,
                    is_question_order_random=True,
                    is_option_order_random=True,
                )
                db.add(quiz)
                db.flush()
                quizzes.append(quiz)

                for qn in range(1, question_count + 1):
                    question = Question(quiz_id=quiz.id, text=f"퀴즈 {i+1} 질문 {qn}")
                    db.add(question)
                    db.flush()

                    if i == 0 and qn == 1:
                        # Add 21 options to the first question of the first quiz
                        db.add_all([
                            Option(question_id=question.id, text=f"선택지 {j+1}", is_correct=(j == 0))
                            for j in range(21)
                        ])
                    else:
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