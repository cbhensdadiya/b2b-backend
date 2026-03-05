# 🚀 How to Run B2B Backend Locally

## Quick Start (Windows)

### Option 1: Use the Batch Script (Easiest)

```bash
cd b2b-backend
run_local.bat
```

That's it! The server will start at http://localhost:8000

### Option 2: Manual Commands

```bash
# 1. Navigate to backend directory
cd b2b-backend

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Start the server
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

---

## 📋 Prerequisites

- Python 3.11 installed
- PostgreSQL running
- Virtual environment created
- Dependencies installed

---

## 🔧 First Time Setup

### 1. Create Virtual Environment

```bash
cd b2b-backend
python -m venv venv
```

### 2. Activate Virtual Environment

```bash
# Windows CMD
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup Database

```bash
# Create database (if not exists)
# Run this in PostgreSQL:
# CREATE DATABASE b2b_marketplace;

# Run migrations
alembic upgrade head
```

### 5. Configure Environment

Copy `.env.example` to `.env` and update:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/b2b_marketplace
SECRET_KEY=your-secret-key-here
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

---

## 🎯 Running the Server

### Development Mode (Auto-reload)

```bash
cd b2b-backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

### Production Mode (Gunicorn)

```bash
cd b2b-backend
venv\Scripts\activate
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Custom Port

```bash
uvicorn app.main:app --reload --port 5000
```

---

## 🧪 Testing the API

### 1. API Documentation

Visit: http://localhost:8000/docs

### 2. Health Check

```bash
curl http://localhost:8000/
```

### 3. Test Endpoints

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

---

## 🗄️ Database Commands

### Run Migrations

```bash
alembic upgrade head
```

### Create New Migration

```bash
alembic revision --autogenerate -m "description"
```

### Rollback Migration

```bash
alembic downgrade -1
```

### Check Current Version

```bash
alembic current
```

---

## 🐛 Troubleshooting

### Error: "No module named 'app'"

**Fix**: Make sure you're in the `b2b-backend` directory

```bash
cd b2b-backend
python test_import.py
```

### Error: "No module named 'src'"

**Fix**: You're running from the wrong directory

```bash
# Should be here:
cd b2b-backend

# NOT here:
cd trading-v1  ← WRONG!
```

### Error: "Database connection failed"

**Fix**: Check your DATABASE_URL in `.env`

```bash
# Make sure PostgreSQL is running
# Check connection string format:
# postgresql://username:password@localhost:5432/database_name
```

### Error: "Port already in use"

**Fix**: Kill the process or use a different port

```bash
# Use different port
uvicorn app.main:app --reload --port 5000
```

---

## 📁 Project Structure

```
b2b-backend/
├── app/
│   ├── __init__.py
│   ├── main.py           ← FastAPI app
│   ├── api/              ← API routes
│   ├── core/             ← Config, database, security
│   ├── models/           ← SQLAlchemy models
│   ├── schemas/          ← Pydantic schemas
│   └── services/         ← Business logic
├── alembic/              ← Database migrations
├── venv/                 ← Virtual environment
├── .env                  ← Environment variables
├── requirements.txt      ← Dependencies
├── alembic.ini          ← Alembic config
└── run_local.bat        ← Quick start script
```

---

## 🔑 Important Commands

### Start Server
```bash
uvicorn app.main:app --reload
```

### Run Migrations
```bash
alembic upgrade head
```

### Test Import
```bash
python test_import.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Activate Venv
```bash
venv\Scripts\activate
```

---

## 🌐 Deployment

For deploying to Render, see:
- `RENDER_FINAL_FIX.md` - Complete deployment guide
- `COPY_PASTE_THIS.txt` - Quick reference
- `DEPLOY_NOW.md` - Step-by-step instructions

---

## 📞 Need Help?

- Check `FIX_LOCAL_ERROR.md` for common errors
- Check `RENDER_FINAL_FIX.md` for deployment issues
- Run `python test_import.py` to diagnose import problems

---

**Last Updated**: March 2026
