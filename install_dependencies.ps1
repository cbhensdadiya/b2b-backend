# PowerShell script to install dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installing Dependencies" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Check if venv exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Green
pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies (binary-only)..." -ForegroundColor Green
pip install --only-binary=:all: --no-cache-dir -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure .env file with your database settings" -ForegroundColor White
Write-Host "2. Run migrations: alembic upgrade head" -ForegroundColor White
Write-Host "3. Start server: uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"
