FROM python:3.12-alpine AS base

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# ---- Install Poetry ----
RUN pip install --no-cache-dir poetry

# ---- Copy only dependency manifests first (leverages Docker layer caching) ----
COPY pyproject.toml poetry.lock* ./

# ---- Install Python deps (no dev deps) ----
RUN apk add --no-cache --virtual .build-deps build-base python3-dev postgresql-dev zlib-dev\
    && poetry install --no-root --only main \
    && apk del .build-deps
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

# ---- Copy application code ----
COPY user_service ./user_service
COPY transaction_service ./transaction_service
COPY common ./common
COPY proto ./proto
COPY user_service/entrypoint.sh .
COPY alembic.ini ./

EXPOSE 50051 9100

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
