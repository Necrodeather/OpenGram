FROM python:3.11.5-slim-bookworm

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ENV POETRY_VERSION=1.6.1

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root --only main

WORKDIR /app/src

CMD ["gunicorn", "-c", "gunicorn.conf.py"]