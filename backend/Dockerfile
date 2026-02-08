# Use official Python 3.11 runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Make scripts executable (if they exist)
RUN chmod +x entrypoint.sh 2>/dev/null || true

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start command with database migration and server startup
CMD python -c "from sqlalchemy import create_engine, text; import os; engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); result = conn.execute(text('SELECT 1')); print('✅ Database connected!'); conn.close()" && \
    alembic upgrade head && \
    uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
