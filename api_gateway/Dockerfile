# ─────────────────────────────────────────────────────────────
# API Gateway – FastAPI / GraphQL / Prometheus
# ─────────────────────────────────────────────────────────────
FROM python:3.12-alpine AS base

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# ---- Install Poetry ----
RUN pip install --no-cache-dir poetry

# ---- Copy only dependency manifests first (leverages Docker layer caching) ----
COPY pyproject.toml poetry.lock* ./
# If you keep api_gateway-specific extras in a separate pyproject, copy that too:
# COPY api_gateway/pyproject.toml api_gateway/poetry.lock* ./api_gateway/

# ---- Install Python deps (no dev deps) ----
RUN apk add --no-cache --virtual .build-deps build-base python3-dev postgresql-dev \
    && poetry install --no-root --only main \
    && apk del .build-deps

# ---- Copy application code ----
COPY api_gateway ./api_gateway
COPY common ./common
COPY proto  ./proto

# ---- Expose gateway port ----
EXPOSE 8000

# ---- Create non-root user for runtime security ----
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# ---- Entrypoint: run Uvicorn ----
# You may tweak workers or reload flags for dev.
CMD ["poetry", "run", "uvicorn", "api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
