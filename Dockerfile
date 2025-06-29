FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root --only main

COPY . .

RUN mkdir -p /code/media /code/staticfiles

EXPOSE 8000