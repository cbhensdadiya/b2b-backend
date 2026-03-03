@echo off
echo ========================================
echo Firebase UID Migration Script
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running database migration...
alembic upgrade head

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ Migration completed successfully!
    echo ========================================
    echo.
    echo Firebase UID field added to users table.
    echo You can now use Firebase authentication.
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ Migration failed!
    echo ========================================
    echo.
    echo Please check the error message above.
    echo.
)

pause
