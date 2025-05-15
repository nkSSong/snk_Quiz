from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    question_count = Column(Integer, nullable=False)  # 출제할 문제 수
    is_question_order_random = Column(Boolean, default=False)
    is_option_order_random = Column(Boolean, default=False)

    questions = relationship("Question", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    text = Column(String, nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question")


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", back_populates="options")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    score = Column(Integer)
    submitted_at = Column(String)

    answers = relationship("Answer", back_populates="result")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey("quiz_results.id", ondelete="CASCADE"))
    question_id = Column(Integer)
    selected_option_id = Column(Integer)

    result = relationship("QuizResult", back_populates="answers")