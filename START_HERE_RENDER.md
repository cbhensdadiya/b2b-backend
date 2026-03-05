# 🚀 Deploy to Render - START HERE

## The Issue

Render keeps running `gunicorn b2b-backend.wsgi` instead of your FastAPI app.

## The Fix (3 Steps)

### Step 1: In Render Dashboard - Settings

**BEFORE deploying, set these:**

1. **Root Directory**: `b2b-backend`
2. **Build Command**:
   ```
   pip install --upgrade pip && pip install --only-binary=:all: --no-cache-dir -r requirements.txt && alembic upgrade head
   ```
3. **Start Command**:
   ```
   gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
   ```

### Step 2: Environment Variables

Add these in Environment tab:

```
DISABLE_COLLECTSTATIC=1
PYTHON_VERSION=3.11.0
DATABASE_URL=<your-postgres-url>
SECRET_KEY=<random-string>
```

### Step 3: Deploy

Click "Manual Deploy"

## Check Logs

Should see:
```
==> Using root directory: b2b-backend
==> Running start command: gunicorn app.main:app...
[INFO] Starting gunicorn 23.0.0
INFO: Application startup complete.
```

## Still Seeing "gunicorn b2b-backend.wsgi"?

1. Delete the service
2. Create NEW service
3. Set Root Directory FIRST
4. Then set Build/Start commands
5. Then deploy

---

**Need detailed help?** Read `RENDER_CRITICAL_FIX.md`
