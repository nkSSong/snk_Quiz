FROM python:3.9-slim

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock* /code/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /code