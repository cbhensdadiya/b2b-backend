# 🔧 Fix: Render Running Wrong Command (Monorepo Issue)

## The Problem

Render is running:
```
gunicorn b2b-backend.wsgi
```

Instead of your configured command:
```
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker
```

This happens because:
1. You're deploying from a monorepo (workspace has both frontend and backend)
2. Render is auto-detecting the app type incorrectly
3. Render is ignoring your start command

---

## ✅ SOLUTION - Manual Configuration (RECOMMENDED)

### Step 1: In Render Dashboard

1. **Go to your service** → Settings

2. **Root Directory** (IMPORTANT!)
   - Set to: `b2b-backend`
   - This tells Render where your backend code is

3. **Build Command**:
   ```bash
   pip install --upgrade pip && pip install --only-binary=:all: --no-cache-dir -r requirements.txt && alembic upgrade head
   ```

4. **Start Command** (Copy exactly):
   ```bash
   gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
   ```

5. **Environment Variables**:
   ```
   PYTHON_VERSION=3.11.0
   PIP_PREFER_BINARY=1
   PIP_ONLY_BINARY=:all:
   DISABLE_COLLECTSTATIC=1
   DATABASE_URL=<your-postgres-url>
   SECRET_KEY=<generate-random>
   ```

6. **Save Changes** and **Manual Deploy**

---

## 🎯 Key Settings Explained

### Root Directory: `b2b-backend`
**Why**: Tells Render to look in the backend folder, not the root
**Without this**: Render looks at root and gets confused by frontend files

### DISABLE_COLLECTSTATIC=1
**Why**: Prevents Django auto-detection
**Without this**: Render thinks you're using Django

### Start Command with Full Path
**Why**: Explicitly tells Render what to run
**Without this**: Render guesses and runs wrong command

---

## 🔍 Verify Configuration

After saving settings, check the deployment logs for:

### ✅ Good Signs:
```
==> Using root directory: b2b-backend
==> Running build command: pip install --upgrade pip...
==> Build succeeded
==> Running start command: gunicorn app.main:app...
[INFO] Starting gunicorn 23.0.0
[INFO] Using worker: uvicorn.workers.UvicornWorker
INFO: Application startup complete.
```

### ❌ Bad Signs:
```
==> Running 'gunicorn b2b-backend.wsgi'  ← WRONG!
ModuleNotFoundError: No module named 'b2b-backend'
```

If you see the bad signs, the Root Directory is not set correctly.

---

## 🚀 Alternative: Deploy Backend Only

If monorepo continues to cause issues, deploy backend separately:

### Option A: Separate Repository
1. Create new repo: `b2b-backend-only`
2. Copy only `b2b-backend/` contents to root
3. Deploy from this repo

### Option B: Use Subdirectory in Render
1. When creating service, select "b2b-backend" as root directory
2. Render will only look at that folder

---

## 📋 Complete Configuration Checklist

In Render Dashboard:

- [ ] **Root Directory**: `b2b-backend` (CRITICAL!)
- [ ] **Build Command**: pip install with --only-binary flag
- [ ] **Start Command**: gunicorn app.main:app with uvicorn workers
- [ ] **Environment Variable**: DISABLE_COLLECTSTATIC=1
- [ ] **Environment Variable**: PYTHON_VERSION=3.11.0
- [ ] **Environment Variable**: DATABASE_URL set
- [ ] **Environment Variable**: SECRET_KEY set
- [ ] **Runtime**: Python 3
- [ ] **Plan**: Free (or your choice)

---

## 🧪 Test Locally First

To verify your start command works:

```bash
cd b2b-backend

# Activate venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test the exact start command
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Should see:
# [INFO] Starting gunicorn 23.0.0
# [INFO] Using worker: uvicorn.workers.UvicornWorker
# INFO: Application startup complete.
```

Visit: http://localhost:8000/docs

If this works locally, it will work on Render (with correct Root Directory set).

---

## 🆘 Still Not Working?

### Check These:

1. **Root Directory is set to `b2b-backend`**
   - Settings → Root Directory
   - Must be exactly: `b2b-backend`

2. **Start Command is correct**
   - Should start with: `gunicorn app.main:app`
   - NOT: `gunicorn b2b-backend.wsgi`

3. **Build logs show correct directory**
   - Should see: "Using root directory: b2b-backend"
   - Should NOT see: "Using root directory: ."

4. **No Django files in backend**
   - No `manage.py`
   - No `wsgi.py` in your app folder
   - No `settings.py` (except in app/core/config.py)

---

## 💡 Pro Tip: Use Procfile

The `Procfile` in your backend folder tells Render what to run:

```
web: gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
```

With Root Directory set to `b2b-backend`, Render will find and use this Procfile automatically.

---

## 📞 Final Checklist Before Deploy

- [ ] Code pushed to GitHub
- [ ] Root Directory = `b2b-backend` in Render settings
- [ ] Build command configured
- [ ] Start command configured (or Procfile exists)
- [ ] DISABLE_COLLECTSTATIC=1 environment variable set
- [ ] DATABASE_URL environment variable set
- [ ] SECRET_KEY environment variable set
- [ ] Manual deploy triggered

---

**Expected Result**: 
```
==> Using root directory: b2b-backend
==> Build succeeded 🎉
==> Starting service
[INFO] Starting gunicorn 23.0.0
[INFO] Using worker: uvicorn.workers.UvicornWorker
INFO: Application startup complete.
==> Your service is live 🎉
```

**Last Updated**: March 2026
