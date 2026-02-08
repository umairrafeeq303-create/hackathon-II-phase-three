#!/bin/bash
# Railway startup script for FastAPI backend

echo "Starting FastAPI application..."
echo "Python version: $(python --version)"
echo "Port: $PORT"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head || echo "Migration failed or no migrations to run"

# Start the application
echo "Starting uvicorn server..."
exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
