FROM python:3.9-slim

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry

COPY . /code/
ENV PYTHONPATH="${PYTHONPATH}:/code"

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-interaction --no-ansi

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]