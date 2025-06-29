#!/bin/sh
set -e

echo "📦 Running Alembic migration..."
alembic upgrade head

echo "🚀 Starting gRPC service..."
exec python -m user_service.grpc_server
