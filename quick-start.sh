#!/usr/bin/env bash
# ------------------------------------------------------------
# Quick bootstrap for Enterprise Money‑Transfer (LOCAL)
# Usage: ./quick-start.sh
# ------------------------------------------------------------
set -euo pipefail

# Optional override
if command -v python3 &>/dev/null; then
    # Prefer python3, which is standard on modern Linux/macOS
    PYTHON_BIN_DEFAULT="python3"
elif command -v python &>/dev/null; then
    # Fallback to python, common on Windows or older systems
    PYTHON_BIN_DEFAULT="python"
else
    echo "❌ Python not found. Please install Python and ensure it's in your PATH." >&2
    exit 1
fi
PYTHON_BIN="${PYTHON_BIN:-$PYTHON_BIN_DEFAULT}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"

log() { printf "\e[1;32m👉 %s\e[0m\n" "$*"; }

# 1️⃣ Ensure Poetry is available
if ! command -v poetry &>/dev/null; then
  log "Installing Poetry locally …"
  curl -sSL https://install.python-poetry.org | $PYTHON_BIN -
  export PATH="$HOME/.local/bin:$PATH"
fi

# 2️⃣ Create venv only inside project
log "Creating local Poetry virtualenv …"
poetry config virtualenvs.in-project true
log "Updating lock file if needed …"
poetry lock
poetry install --no-root --no-interaction
poetry sync

# 3️⃣ Generate gRPC stubs
log "Generating gRPC stubs …"
poetry run python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/userprofile.proto proto/banktransaction.proto

# 4️⃣ Build and run stack
log "Launching Docker stack …"
docker compose -f "$COMPOSE_FILE" build --quiet
docker compose -f "$COMPOSE_FILE" up -d

log "✅ Stack is running!"
echo "➡️  REST + GraphQL: http://localhost:8000"
echo "➡️  Swagger:        http://localhost:8000/docs"
echo "➡️  Keycloak:       http://localhost:8080"
echo "➡️  Grafana:        http://localhost:3000"
