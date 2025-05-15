import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.database import Base
from app.user.domain.models import User
from app.quiz.domain.models import Quiz, Question, Option, QuizResult, Answer


from dotenv import load_dotenv

load_dotenv()

# 👉 async URL 예: postgresql+asyncpg://user:pass@db:5432/dbname
# 👇 sync URL 예: postgresql://user:pass@db:5432/dbname
db_url = os.getenv("DATABASE_URL").replace("+asyncpg", "")

config = context.config
config.set_main_option("sqlalchemy.url", db_url)

fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()