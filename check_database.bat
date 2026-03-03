@echo off
echo ========================================
echo Database Column Check
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Checking if firebase_uid column exists...
python check_firebase_uid_column.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ Database is ready!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ❌ Database needs migration!
    echo ========================================
    echo.
    echo Run this command to fix:
    echo   apply_firebase_migration.bat
    echo.
)

pause
