FROM python:3.12-slim

WORKDIR /code

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

RUN mkdir -p /code/media

EXPOSE 8000