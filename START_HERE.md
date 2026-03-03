# 🚀 START HERE - Quick Setup Guide

Get your B2B Marketplace backend running in 5 minutes!

---

## Prerequisites

✅ Python 3.11+ installed  
✅ PostgreSQL 14+ installed  
✅ pip installed  

---

## Quick Setup (Windows)

### Option 1: Automated Setup (Easiest)

Just run this:

```bash
setup.bat
```

This will:
- Create virtual environment
- Install dependencies
- Create .env file
- Set up database
- Run migrations
- Seed admin

### Option 2: Step by Step

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
copy .env.example .env

# 4. Edit .env with your PostgreSQL password
notepad .env

# 5. Run database setup
python setup_database.py

# 6. Start server
uvicorn app.main:app --reload
```

---

## Quick Setup (Linux/Mac)

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Edit .env with your PostgreSQL password
nano .env

# 5. Run database setup
python setup_database.py

# 6. Start server
uvicorn app.main:app --reload
```

---

## Manual Database Setup

If automated setup doesn't work:

### 1. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE b2b_marketplace;

# Exit
\q
```

### 2. Update .env File

Edit `.env` and update:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/b2b_marketplace
DB_PASSWORD=YOUR_PASSWORD
```

### 3. Run Migrations

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Seed Master Admin

```bash
python seed_admin.py
```

---

## Verify Setup

### 1. Test Database Connection

```bash
python test_setup.py
```

Should show all tests passing ✓

### 2. Start Server

```bash
uvicorn app.main:app --reload
```

Should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 3. Open Swagger UI

Open browser: http://localhost:8000/docs

You should see the API documentation!

### 4. Test API

Try the signup endpoint:
- Click "POST /api/buyer/auth/signup"
- Click "Try it out"
- Fill in the form
- Click "Execute"

---

## Master Admin Credentials

**Email:** cbhensdadiya@sofvare.com  
**Password:** cp@512A

⚠️ Change these in production!

---

## Common Issues

### Issue: "psql: command not found"

**Fix:** Add PostgreSQL to PATH
- Windows: `C:\Program Files\PostgreSQL\14\bin`
- Mac: `brew install postgresql`
- Linux: `sudo apt install postgresql`

### Issue: "password authentication failed"

**Fix:** Check password in .env file matches PostgreSQL password

### Issue: "could not connect to server"

**Fix:** Make sure PostgreSQL is running
- Windows: Check Services app
- Mac: `brew services start postgresql`
- Linux: `sudo systemctl start postgresql`

### Issue: "ImportError: No module named 'psycopg2'"

**Fix:** 
```bash
pip install psycopg2-binary
```

---

## Next Steps

1. ✅ Backend running at http://localhost:8000
2. ✅ API docs at http://localhost:8000/docs
3. 📱 Update Angular frontend API URL
4. 🧪 Test authentication flow
5. 🎉 Start building!

---

## File Structure

```
b2b-backend/
├── app/                    # Application code
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic
├── alembic/               # Database migrations
├── .env                   # Configuration (create this)
├── requirements.txt       # Dependencies
├── setup_database.py      # Database setup script
└── seed_admin.py         # Admin seeding script
```

---

## Quick Commands

```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Start server
uvicorn app.main:app --reload

# Run migrations
alembic upgrade head

# Seed admin
python seed_admin.py

# Test setup
python test_setup.py

# Create new migration
alembic revision --autogenerate -m "description"
```

---

## Documentation

- 📖 **README.md** - Complete documentation
- 🚀 **QUICKSTART.md** - Quick start guide
- 💾 **DATABASE_SETUP.md** - Database setup details
- 🔌 **INTEGRATION_GUIDE.md** - Frontend integration
- 🧪 **API_TESTING.md** - API testing guide
- 📊 **PROJECT_SUMMARY.md** - Project overview

---

## Support

Need help?

1. Check **DATABASE_SETUP.md** for detailed database setup
2. Check **QUICKSTART.md** for step-by-step guide
3. Run `python test_setup.py` to diagnose issues
4. Check backend console for error messages

---

## Success Checklist

- [ ] PostgreSQL installed and running
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file created
- [ ] Database created
- [ ] Migrations applied
- [ ] Master admin seeded
- [ ] Server starts without errors
- [ ] Swagger UI accessible
- [ ] Test API endpoint works

---

**Ready to go! 🎉**

Start the server and open http://localhost:8000/docs to explore the API!
