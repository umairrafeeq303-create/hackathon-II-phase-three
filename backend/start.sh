#!/bin/bash
# Railway startup script for FastAPI backend

set -e  # Exit immediately if a command exits with non-zero status

echo "=========================================="
echo "🚀 FastAPI Backend Startup"
echo "=========================================="
echo "Python: $(python --version)"
echo "Pip: $(pip --version)"
echo "Port: ${PORT:-8000}"
echo "Environment: ${ENVIRONMENT:-production}"
echo "=========================================="

# Step 1: Test database connection
echo ""
echo "📡 Testing database connection..."
python -c "
from sqlalchemy import create_engine, text
import os
import sys

try:
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print('❌ DATABASE_URL not set!')
        sys.exit(1)

    # Hide password in output
    safe_url = db_url
    if '@' in db_url and ':' in db_url.split('@')[0]:
        user_pass = db_url.split('@')[0].split('://')[1]
        user = user_pass.split(':')[0]
        safe_url = db_url.replace(user_pass, f'{user}:****')

    print(f'Database: {safe_url}')

    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
        print('✅ Database connection successful!')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    print('⚠️  Please check your DATABASE_URL environment variable')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Startup aborted due to database connection failure"
    exit 1
fi

# Step 2: Run database migrations
echo ""
echo "📊 Running database migrations..."
alembic upgrade head || {
    echo "⚠️  Migration warning (may be OK if no migrations exist)"
}

# Step 3: Start the application
echo ""
echo "🌐 Starting uvicorn server..."
echo "Command: uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"
echo "=========================================="
exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
