FROM python:3.12-slim

WORKDIR /code

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY . .

RUN mkdir -p /code/media

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]