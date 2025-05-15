# app/core/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from contextlib import asynccontextmanager
import os

# Async database setup
ASYNC_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/snkquiz")
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync database setup (for Alembic, seed, etc.)
SYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("+asyncpg", "")
sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(bind=sync_engine))

Base = declarative_base()

# Sync get_db (for seed, Alembic)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async get_db (for FastAPI dependency)
@asynccontextmanager
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session