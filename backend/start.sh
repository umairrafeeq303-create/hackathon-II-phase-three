#!/bin/bash
# Railway startup script for FastAPI backend

set -e  # Exit on error

echo "========================================="
echo "Starting FastAPI application..."
echo "========================================="
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo "Port: ${PORT:-8000}"
echo "Environment: ${ENVIRONMENT:-development}"
echo "========================================="

# Run database migrations
echo "Running database migrations..."
alembic upgrade head || {
    echo "⚠️  Migration failed or no migrations to run"
}

# Start the application
echo "Starting uvicorn server..."
echo "Command: uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"
exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
