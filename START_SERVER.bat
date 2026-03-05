@echo off
cls
echo ========================================
echo B2B Backend - Start Server
echo ========================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if we're in the right place
if not exist "app\main.py" (
    echo ERROR: app\main.py not found!
    echo You must run this script from the b2b-backend directory.
    echo.
    pause
    exit /b 1
)

echo Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create it first: python -m venv venv
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo ========================================
echo Starting FastAPI Server
echo ========================================
echo.
echo Server will start at: http://localhost:8000
echo API Docs will be at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server with the CORRECT command
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
