# PowerShell script to run database migrations

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Database Migrations" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Check if venv exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run install_dependencies.ps1 first" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Run migrations
Write-Host ""
Write-Host "Running alembic upgrade head..." -ForegroundColor Green
alembic upgrade head

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Migrations Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"
