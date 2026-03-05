#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies with binary-only flag to avoid Rust compilation
pip install --only-binary=:all: --no-cache-dir -r requirements.txt

# Run database migrations
alembic upgrade head

echo "Build completed successfully!"
