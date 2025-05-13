# app/core/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from sqlalchemy import create_engine  # ← sync용 추가
from sqlalchemy.orm import scoped_session

import os

# Async 사용 시 이 엔진 사용
ASYNC_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/snkquiz")
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 👉 Seed나 Alembic처럼 sync 접근 시 이 엔진 사용
SYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("+asyncpg", "")
sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(bind=sync_engine))

Base = declarative_base()