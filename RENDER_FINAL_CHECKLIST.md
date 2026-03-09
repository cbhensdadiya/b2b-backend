# ✅ Render Deployment - Final Checklist

## Copy These EXACT Settings to Render Dashboard

### 1. Root Directory
```
b2b-backend
```
⚠️ This is THE MOST IMPORTANT setting!

### 2. Build Command
```bash
pip install --upgrade pip && pip install --only-binary=:all: --no-cache-dir -r requirements.txt && alembic upgrade head
```

### 3. Start Command
```bash
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile - --log-level info
```

### 4. Environment Variables

Add these ONE BY ONE in the Environment tab:

```
PYTHON_VERSION=3.11.0
PIP_PREFER_BINARY=1
PIP_ONLY_BINARY=:all:
DISABLE_COLLECTSTATIC=1
DATABASE_URL=<your-postgres-internal-url>
SECRET_KEY=<generate-with-openssl-rand-hex-32>
```

---

## 🎯 Step-by-Step Instructions

### Step 1: Create/Update Service

1. Go to Render Dashboard
2. If service exists: Go to Settings
3. If new: Click "New +" → "Web Service"

### Step 2: Configure Root Directory FIRST

1. Settings → **Root Directory**
2. Type: `b2b-backend`
3. Click "Save Changes"

### Step 3: Configure Build & Deploy

1. Settings → **Build & Deploy**
2. **Build Command**: Paste the build command above
3. **Start Command**: Paste the start command above
4. Click "Save Changes"

### Step 4: Add Environment Variables

1. Go to **Environment** tab
2. Click "Add Environment Variable"
3. Add each variable from the list above
4. Click "Save Changes"

### Step 5: Create Database (if not exists)

1. Click "New +" → "PostgreSQL"
2. Name: `b2b-database`
3. Plan: Free
4. Click "Create Database"
5. Copy the "Internal Database URL"
6. Add it as `DATABASE_URL` in your web service

### Step 6: Generate SECRET_KEY

Run in your terminal:
```bash
openssl rand -hex 32
```
Copy the output and add as `SECRET_KEY` environment variable

### Step 7: Deploy

1. Click "Manual Deploy"
2. Select "Deploy latest commit"
3. Wait for build to complete (2-5 minutes)

---

## ✅ Verification - Check Logs

### Good Signs (Success):
```
==> Using root directory: b2b-backend
==> Installing dependencies
Successfully installed gunicorn-23.0.0 pydantic-2.9.2 ...
==> Running migrations
INFO  [alembic.runtime.migration] Running upgrade
==> Build succeeded 🎉
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

### Bad Signs (Errors):
```
❌ Running 'gunicorn b2b-backend.wsgi'
   → Root Directory not set correctly

❌ Could not import module "main"
   → Start command should be "app.main:app" not "main:app"

❌ ModuleNotFoundError: No module named 'b2b-backend'
   → Root Directory not set to "b2b-backend"

❌ Read-only file system (os error 30)
   → Missing PIP_ONLY_BINARY environment variable

❌ Database connection failed
   → DATABASE_URL not set or incorrect
```

---

## 🧪 Test After Deployment

### 1. Health Check
```bash
curl https://your-app.onrender.com/
```

### 2. API Documentation
Visit: `https://your-app.onrender.com/docs`

### 3. Check Logs
Look for "Application startup complete" message

---

## 🆘 Troubleshooting

### Issue: "Using root directory: ." (wrong!)
**Fix**: Root Directory must be set to `b2b-backend`

### Issue: "gunicorn b2b-backend.wsgi"
**Fix**: 
1. Set Root Directory to `b2b-backend`
2. Add `DISABLE_COLLECTSTATIC=1` environment variable
3. Verify Start Command is correct

### Issue: "Could not import module 'main'"
**Fix**: Start Command must use `app.main:app` not `main:app`

### Issue: Build fails with Rust compilation error
**Fix**: Add these environment variables:
- `PIP_PREFER_BINARY=1`
- `PIP_ONLY_BINARY=:all:`

### Issue: Database connection failed
**Fix**: 
1. Create PostgreSQL database in Render
2. Copy "Internal Database URL"
3. Add as `DATABASE_URL` environment variable

---

## 📋 Final Verification Checklist

Before deploying, verify:

- [ ] Root Directory = `b2b-backend` (NOT empty, NOT `.`)
- [ ] Build Command contains `--only-binary=:all:`
- [ ] Start Command starts with `gunicorn app.main:app`
- [ ] Start Command contains `uvicorn.workers.UvicornWorker`
- [ ] PYTHON_VERSION=3.11.0 is set
- [ ] PIP_PREFER_BINARY=1 is set
- [ ] PIP_ONLY_BINARY=:all: is set
- [ ] DISABLE_COLLECTSTATIC=1 is set
- [ ] DATABASE_URL is set (from PostgreSQL database)
- [ ] SECRET_KEY is set (generated with openssl)

---

## 🎉 Success Indicators

After successful deployment:

1. ✅ Service status shows "Live"
2. ✅ Logs show "Application startup complete"
3. ✅ Health endpoint responds: `https://your-app.onrender.com/`
4. ✅ API docs load: `https://your-app.onrender.com/docs`
5. ✅ No errors in logs

---

## 📞 Still Having Issues?

1. **Screenshot your settings**: Root Directory, Build Command, Start Command
2. **Copy full error logs**: From build or runtime logs
3. **Verify environment variables**: All required vars are set
4. **Check database**: PostgreSQL is running and URL is correct

---

**Last Updated**: March 2026
**Status**: Ready for deployment
