#!/usr/bin/env bash
# Start script for Render deployment

echo "Starting B2B Backend with Gunicorn + Uvicorn workers..."
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"

# Start the application
exec gunicorn app.main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:${PORT:-8000} \
    --access-logfile - \
    --error-logfile - \
    --log-level info
