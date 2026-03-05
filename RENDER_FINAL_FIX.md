# ✅ FINAL FIX - Correct Start Command

## Current Error

```
Running 'uvicorn main:app --host 0.0.0.0 --port 10000'
ERROR: Error loading ASGI app. Could not import module "main".
```

## The Problem

Render is running `uvicorn main:app` but your FastAPI app is at `app.main:app`

The file structure is:
```
b2b-backend/
  └── app/
      └── main.py  ← FastAPI app is here
```

So the import path must be `app.main:app` (not `main:app`)

---

## ✅ THE FIX - Update Start Command

### In Render Dashboard:

1. **Go to your service**
2. **Settings** → **Build & Deploy**
3. **Start Command** - Change to:

```bash
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
```

OR if you prefer uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2
```

4. **Click "Save Changes"**
5. **Click "Manual Deploy"**

---

## 🎯 Key Points

### ✅ CORRECT Commands:
```bash
# Option 1: Gunicorn + Uvicorn workers (RECOMMENDED for production)
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT

# Option 2: Uvicorn directly (simpler, but less robust)
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### ❌ WRONG Commands:
```bash
uvicorn main:app          # ← Missing 'app.' prefix
gunicorn main:app         # ← Missing 'app.' prefix
python -m uvicorn main:app # ← Missing 'app.' prefix
```

---

## 📋 Complete Configuration Checklist

Make sure ALL these are set in Render Dashboard:

### 1. Root Directory
```
b2b-backend
```

### 2. Build Command
```bash
pip install --upgrade pip && pip install --only-binary=:all: --no-cache-dir -r requirements.txt && alembic upgrade head
```

### 3. Start Command (CHOOSE ONE)

**Option A - Gunicorn (Recommended):**
```bash
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
```

**Option B - Uvicorn (Simpler):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2
```

### 4. Environment Variables
```
PYTHON_VERSION=3.11.0
PIP_PREFER_BINARY=1
PIP_ONLY_BINARY=:all:
DISABLE_COLLECTSTATIC=1
DATABASE_URL=<your-postgres-url>
SECRET_KEY=<random-string>
```

---

## ✅ Expected Success Output

After fixing the start command, you should see:

### With Gunicorn:
```
==> Using root directory: b2b-backend
==> Build succeeded
==> Running start command: gunicorn app.main:app...
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: uvicorn.workers.UvicornWorker
[INFO] Booting worker with pid: 123
INFO:     Started server process [123]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
==> Your service is live 🎉
```

### With Uvicorn:
```
==> Using root directory: b2b-backend
==> Build succeeded
==> Running start command: uvicorn app.main:app...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
==> Your service is live 🎉
```

---

## 🧪 Test Locally

To verify the command works:

```bash
cd b2b-backend

# Activate venv
venv\Scripts\activate

# Test with gunicorn
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# OR test with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs

If this works locally, it will work on Render!

---

## 🎉 After Successful Deploy

Test these endpoints:

1. **Health Check**: `https://your-app.onrender.com/`
2. **API Docs**: `https://your-app.onrender.com/docs`
3. **OpenAPI**: `https://your-app.onrender.com/openapi.json`

---

## 📝 Summary

The fix is simple: Change `main:app` to `app.main:app` in your start command.

This tells Python to:
1. Look in the `app` package (folder)
2. Import the `main` module (main.py file)
3. Use the `app` variable (FastAPI instance)

---

**Last Updated**: March 2026
**Status**: ✅ This should fix your deployment!
