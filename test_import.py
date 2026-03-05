#!/usr/bin/env python
"""Test if app.main can be imported correctly"""

import sys
import os

print("=" * 50)
print("Testing Import Path")
print("=" * 50)
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path[:3]}")
print()

try:
    print("Attempting to import app.main...")
    import app.main
    print("✅ SUCCESS: app.main imported successfully!")
    print(f"✅ FastAPI app found: {app.main.app}")
    print()
    print("Your app is ready to run!")
    print()
    print("Run with:")
    print("  uvicorn app.main:app --reload")
    print("  OR")
    print("  gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker")
except ImportError as e:
    print(f"❌ ERROR: {e}")
    print()
    print("Make sure you're running this from the b2b-backend directory!")
    print("Current directory should contain:")
    print("  - app/ folder")
    print("  - requirements.txt")
    print("  - alembic.ini")
    sys.exit(1)

print("=" * 50)
