#!/bin/bash
# Production entrypoint script with database validation
# Ensures database is accessible before starting the application

set -e  # Exit immediately if a command exits with non-zero status

echo "=========================================="
echo "🚀 Starting FastAPI Application"
echo "=========================================="
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo "Port: ${PORT:-8000}"
echo "Environment: ${ENVIRONMENT:-production}"
echo "=========================================="

# Step 1: Test database connection
echo ""
echo "📡 Step 1: Testing database connection..."
python test_connection.py
if [ $? -ne 0 ]; then
    echo "❌ Database connection test failed!"
    echo "⚠️  Application cannot start without database access"
    echo "Please check your DATABASE_URL environment variable"
    exit 1
fi

# Step 2: Run database migrations
echo ""
echo "📊 Step 2: Running database migrations..."
alembic upgrade head
if [ $? -ne 0 ]; then
    echo "⚠️  Migration failed, but continuing (migrations may not exist yet)"
fi

# Step 3: Start the application
echo ""
echo "🌐 Step 3: Starting uvicorn server..."
echo "Command: uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"
echo "=========================================="
exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
