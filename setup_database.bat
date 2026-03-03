@echo off
REM Quick Database Setup Script for Windows

echo ============================================================
echo PostgreSQL Database Setup
echo ============================================================
echo.

REM Get database credentials
set /p DB_USER="PostgreSQL Username [postgres]: " || set DB_USER=postgres
set /p DB_PASSWORD="PostgreSQL Password: "
set /p DB_NAME="Database Name [b2b_marketplace]: " || set DB_NAME=b2b_marketplace

echo.
echo Creating database...
echo.

REM Set password environment variable
set PGPASSWORD=%DB_PASSWORD%

REM Create database
psql -U %DB_USER% -c "CREATE DATABASE %DB_NAME%;"

if errorlevel 1 (
    echo.
    echo Database might already exist or creation failed
    echo Continuing with existing database...
)

echo.
echo Database created/verified: %DB_NAME%
echo.

REM Update .env file
echo Updating .env file...
powershell -Command "(Get-Content .env) -replace 'DB_PASSWORD=password', 'DB_PASSWORD=%DB_PASSWORD%' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace 'DB_USER=postgres', 'DB_USER=%DB_USER%' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace 'DB_NAME=b2b_marketplace', 'DB_NAME=%DB_NAME%' | Set-Content .env"

echo.
echo Running migrations...
call venv\Scripts\activate.bat
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

if errorlevel 1 (
    echo.
    echo [ERROR] Migrations failed
    pause
    exit /b 1
)

echo.
echo Seeding master admin...
python seed_admin.py

if errorlevel 1 (
    echo.
    echo [ERROR] Admin seeding failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Database Setup Complete!
echo ============================================================
echo.
echo Database: %DB_NAME%
echo User: %DB_USER%
echo.
echo Master Admin Credentials:
echo   Email: cbhensdadiya@sofvare.com
echo   Password: cp@512A
echo.
echo Next: Start the server with:
echo   uvicorn app.main:app --reload
echo.
pause
