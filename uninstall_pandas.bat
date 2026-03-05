@echo off
echo ========================================
echo Uninstalling pandas from virtual environment
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Uninstalling pandas...
pip uninstall pandas -y

echo.
echo ========================================
echo Pandas uninstalled successfully!
echo ========================================
echo.
echo Press any key to exit...
pause >nul
