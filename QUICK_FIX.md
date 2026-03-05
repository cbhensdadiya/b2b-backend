# 🚀 QUICK FIX for Render Deployment Errors

## Problem 1: Rust Compilation Error
```
failed to create directory `/usr/local/cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`
Read-only file system (os error 30)
```

## Problem 2: Gunicorn Not Found
```
bash: line 1: gunicorn: command not found
```

Both issues are now FIXED!

---

## ✅ SOLUTION - Manual Setup in Render Dashboard

### Step 1: Update Your Code
```bash
git add .
git commit -m "Fix Render deployment - add gunicorn and correct config"
git push
```

### Step 2: Configure in Render Dashboard

1. **Go to your service** → Settings → Build & Deploy

2. **Set Build Command**:
   ```bash
   pip install --upgrade pip && pip install --only-binary=:all: --no-cache-dir -r requirements.txt && alembic upgrade head
   ```

3. **Set Start Command**:
   ```bash
   gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

4. **Add Environment Variables** (Environment tab):
   ```
   PYTHON_VERSION=3.11.0
   PIP_PREFER_BINARY=1
   PIP_ONLY_BINARY=:all:
   DATABASE_URL=<your-postgres-url>
   SECRET_KEY=<generate-with-openssl-rand-hex-32>
   ```

5. **Save and Deploy**
   - Click "Save Changes"
   - Click "Manual Deploy" → "Deploy latest commit"

---

## 🎯 What Was Fixed

### requirements.txt
- ✅ Added gunicorn==23.0.0 (production WSGI server)
- ✅ Updated pydantic to 2.9.2 (pre-built wheels)
- ✅ Added explicit pydantic-core 2.23.4
- ✅ Updated FastAPI and uvicorn

### Configuration Files
- ✅ Created `Procfile` with correct start command
- ✅ Updated `render.yaml` with gunicorn + uvicorn workers
- ✅ Updated `build.sh` with migrations
- ✅ Added `runtime.txt` for Python 3.11

---

## 🔄 Alternative: Use Blueprint (render.yaml)

If you prefer automated setup:

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment config"
   git push
   ```

2. **In Render Dashboard**:
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Select `b2b-backend` folder (if monorepo)
   - Render will use `render.yaml` automatically
   - Click "Apply"

3. **Set Environment Variables**:
   - DATABASE_URL (auto-set if using render.yaml database)
   - SECRET_KEY (generate: `openssl rand -hex 32`)
   - TWILIO_* (if using SMS)

---

## 📋 Why Gunicorn?

**Gunicorn + Uvicorn Workers = Production Ready**

- Gunicorn: Process manager (handles multiple workers)
- Uvicorn: ASGI server (handles async FastAPI)
- Together: Better performance, auto-restart, graceful shutdown

**Start Command Explained**:
```bash
gunicorn app.main:app \
  --workers 2 \                              # 2 worker processes
  --worker-class uvicorn.workers.UvicornWorker \  # Use Uvicorn for async
  --bind 0.0.0.0:$PORT                       # Bind to Render's port
```

---

## 🧪 Test Locally

```bash
cd b2b-backend

# Activate venv
venv\Scripts\activate

# Install updated requirements
pip install -r requirements.txt

# Test with gunicorn (like production)
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or test with uvicorn (development)
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

---

## ✅ Expected Result

After deployment, you should see:

```
==> Installing dependencies
Successfully installed gunicorn-23.0.0 pydantic-2.9.2 pydantic-core-2.23.4 ...
==> Running migrations
INFO  [alembic.runtime.migration] Running upgrade -> a9bde1ae2c6e
==> Build succeeded 🎉
==> Starting service with command: gunicorn app.main:app ...
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: uvicorn.workers.UvicornWorker
[INFO] Booting worker with pid: 123
[INFO] Started server process [123]
[INFO] Application startup complete.
```

---

## 🎯 Quick Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] Build command set correctly
- [ ] Start command set correctly
- [ ] Environment variables added
- [ ] PostgreSQL database created
- [ ] DATABASE_URL connected

After deploying:
- [ ] Check build logs (should see "Build succeeded")
- [ ] Check runtime logs (should see "Application startup complete")
- [ ] Test health endpoint: `https://your-app.onrender.com/`
- [ ] Test API docs: `https://your-app.onrender.com/docs`

---

## ⚠️ Common Issues

### "gunicorn: command not found"
**Fix**: Make sure `gunicorn==23.0.0` is in requirements.txt (already added)

### "Module 'app.main' not found"
**Fix**: Make sure you're in the correct directory. If monorepo, set `rootDir: b2b-backend` in render.yaml

### "Database connection failed"
**Fix**: 
1. Create PostgreSQL database in Render
2. Copy "Internal Database URL"
3. Set as `DATABASE_URL` environment variable

### "Port already in use"
**Fix**: Use `$PORT` variable in start command (already configured)

---

## 📞 Still Having Issues?

1. Check build logs in Render Dashboard
2. Check runtime logs for errors
3. Verify all environment variables are set
4. Test database connection
5. Check full guide: `RENDER_DEPLOYMENT.md`

---

**Last Updated**: March 2026
