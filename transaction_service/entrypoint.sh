#!/bin/sh
set -e

echo "📦 Running Alembic migration..."
alembic upgrade head

echo "🚀 Starting gRPC service..."
exec python grpc_server.py
