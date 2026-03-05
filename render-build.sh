#!/usr/bin/env bash
# exit on error
set -o errexit

echo "========================================="
echo "Starting Render Build Process"
echo "========================================="
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies with binary-only flag
echo "Installing dependencies (binary-only)..."
pip install --only-binary=:all: --no-cache-dir -r requirements.txt

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

echo ""
echo "========================================="
echo "Build completed successfully!"
echo "========================================="
