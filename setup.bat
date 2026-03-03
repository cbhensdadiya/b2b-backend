@echo off
REM B2B Marketplace Backend - Quick Setup Script for Windows
REM This script automates the setup process

echo ============================================================
echo B2B Marketplace Backend - Quick Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11 or higher
    pause
    exit /b 1
)

echo [1/7] Python found
echo.

REM Check if PostgreSQL is installed
psql --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL is not installed or not in PATH
    echo Please install PostgreSQL 14 or higher
    echo Download from: https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)

echo [2/7] PostgreSQL found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [3/7] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo [3/7] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [4/7] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [5/7] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed
echo.

REM Check if .env exists
if not exist ".env" (
    echo [6/7] Creating .env file...
    copy .env.example .env
    echo.
    echo ============================================================
    echo IMPORTANT: Please edit .env file with your settings
    echo ============================================================
    echo.
    echo Update these values in .env:
    echo - DATABASE_URL (PostgreSQL connection string)
    echo - DB_PASSWORD (your PostgreSQL password)
    echo - SECRET_KEY (generate a strong key)
    echo.
    echo After editing .env, run: setup_database.bat
    echo ============================================================
    pause
    exit /b 0
) else (
    echo [6/7] .env file already exists
)
echo.

REM Run database setup
echo [7/7] Setting up database...
echo.
python setup_database.py
if errorlevel 1 (
    echo.
    echo [ERROR] Database setup failed
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Backend is ready to run!
echo.
echo To start the server:
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload
echo.
echo Then open: http://localhost:8000/docs
echo.
pause
