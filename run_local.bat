@echo off
echo ========================================
echo Starting B2B Backend Locally
echo ========================================
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Testing import...
python test_import.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Import test failed!
    echo Make sure you're in the b2b-backend directory.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting server with uvicorn...
echo ========================================
echo.
echo Visit: http://localhost:8000/docs
echo Press Ctrl+C to stop
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
