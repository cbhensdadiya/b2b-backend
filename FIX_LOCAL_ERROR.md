# Fix: ModuleNotFoundError: No module named 'src'

## The Error

```
ModuleNotFoundError: No module named 'src'
```

This error happens when you're running uvicorn from the wrong directory.

---

## ✅ SOLUTION

### Step 1: Make Sure You're in the Right Directory

```bash
# You should be HERE:
cd b2b-backend

# NOT here:
# cd trading-v1  ← WRONG!
```

### Step 2: Check Your Current Directory

```bash
# Windows PowerShell or CMD
cd

# Should show something like:
# C:\CP\BVSS\trading-v1\b2b-backend
```

The path should END with `b2b-backend`

### Step 3: Run the Test Script

```bash
python test_import.py
```

Should output:
```
✅ SUCCESS: app.main imported successfully!
```

### Step 4: Start the Server

```bash
# Activate venv first
venv\Scripts\activate

# Then run uvicorn
uvicorn app.main:app --reload
```

---

## 🚀 Easy Way: Use the Batch Script

Just double-click or run:

```bash
run_local.bat
```

This script:
1. Changes to the correct directory
2. Activates the virtual environment
3. Tests the import
4. Starts the server

---

## 🔍 Why This Happens

The error occurs because:

1. **Wrong Directory**: You're running uvicorn from `trading-v1/` instead of `trading-v1/b2b-backend/`

2. **Python Can't Find `app` Module**: When you're in the wrong directory, Python can't find the `app/` folder

3. **Uvicorn Looks for `src`**: Some error in the import chain is looking for a `src` module that doesn't exist

---

## 📋 Correct Directory Structure

Your directory should look like this:

```
b2b-backend/          ← YOU SHOULD BE HERE
├── app/              ← Python needs to find this
│   ├── __init__.py
│   ├── main.py       ← Your FastAPI app
│   ├── api/
│   ├── core/
│   ├── models/
│   └── schemas/
├── alembic/
├── venv/
├── requirements.txt
└── run_local.bat     ← Run this
```

---

## ✅ Verification Checklist

Run these commands to verify:

```bash
# 1. Check current directory
cd
# Should end with: b2b-backend

# 2. List files
dir
# Should see: app, alembic, venv, requirements.txt

# 3. Check if app folder exists
dir app
# Should see: main.py, api, core, models, schemas

# 4. Test import
python -c "import app.main; print('OK')"
# Should print: OK
```

---

## 🆘 Still Not Working?

### Option 1: Use Full Path

```bash
cd C:\CP\BVSS\trading-v1\b2b-backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

### Option 2: Check Python Path

```bash
python -c "import sys; print('\n'.join(sys.path))"
```

The current directory (`.`) should be in the list.

### Option 3: Reinstall Dependencies

```bash
cd b2b-backend
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎯 Quick Commands

### Start Development Server:
```bash
cd b2b-backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

### Start with Gunicorn (Production-like):
```bash
cd b2b-backend
venv\Scripts\activate
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Run Migrations:
```bash
cd b2b-backend
venv\Scripts\activate
alembic upgrade head
```

---

## 📝 Summary

The fix is simple:
1. **Always run commands from the `b2b-backend` directory**
2. **Use `app.main:app` (not `main:app` or `src.main:app`)**
3. **Activate venv before running**

---

**Last Updated**: March 2026
