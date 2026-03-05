# 🚨 CRITICAL FIX: Render Ignoring Start Command

## The Problem

Render keeps running:
```
gunicorn b2b-backend.wsgi
```

Even though you've configured a different start command. This is because:
1. Render's auto-detection is overriding your settings
2. The Root Directory might not be set correctly
3. Render thinks this is a Django app

---

## ✅ SOLUTION: Force Override in Dashboard

You MUST manually configure these settings in Render Dashboard. The files alone won't work.

### Step 1: Delete and Recreate Service (RECOMMENDED)

Sometimes Render caches the wrong detection. Fresh start fixes this:

1. **Delete the current service** in Render Dashboard
2. **Create a NEW Web Service**
3. **Connect your repository**
4. **IMMEDIATELY configure these settings BEFORE first deploy:**

---

### Step 2: Configure Settings (CRITICAL - DO THIS FIRST!)

#### A. Root Directory
**Settings → Root Directory:**
```
b2b-backend
```
⚠️ Set this FIRST before anything else!

#### B. Build Command
**Settings → Build & Deploy → Build Command:**
```bash
chmod +x render-build.sh && ./render-build.sh
```

OR if that doesn't work:
```bash
pip install --upgrade pip && pip install --only-binary=:all: --no-cache-dir -r requirements.txt && alembic upgrade head
```

#### C. Start Command
**Settings → Build & Deploy → Start Command:**
```bash
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
```

⚠️ **CRITICAL**: Make sure this is EXACTLY as shown. No typos!

#### D. Environment Variables
**Environment tab → Add these ONE BY ONE:**

```
PYTHON_VERSION=3.11.0
PIP_PREFER_BINARY=1
PIP_ONLY_BINARY=:all:
DISABLE_COLLECTSTATIC=1
```

**Required:**
```
DATABASE_URL=<your-postgres-url>
SECRET_KEY=<generate-with-openssl-rand-hex-32>
```

---

### Step 3: Verify Before Deploying

Before clicking "Create Web Service" or "Manual Deploy", verify:

- [ ] Root Directory = `b2b-backend` (NOT empty, NOT `.`)
- [ ] Build Command starts with `pip install` or `chmod +x render-build.sh`
- [ ] Start Command starts with `gunicorn app.main:app`
- [ ] Start Command does NOT contain `b2b-backend.wsgi`
- [ ] DISABLE_COLLECTSTATIC=1 is set
- [ ] DATABASE_URL is set
- [ ] SECRET_KEY is set

---

### Step 4: Deploy and Check Logs

Click "Manual Deploy" and watch the logs carefully:

#### ✅ GOOD - You should see:
```
==> Using root directory: b2b-backend
==> Running build command: pip install...
==> Build succeeded
==> Running start command: gunicorn app.main:app...
[INFO] Starting gunicorn 23.0.0
[INFO] Using worker: uvicorn.workers.UvicornWorker
INFO: Application startup complete.
```

#### ❌ BAD - If you see this:
```
==> Running 'gunicorn b2b-backend.wsgi'
ModuleNotFoundError: No module named 'b2b-backend'
```

**This means Render is STILL ignoring your settings!**

---

## 🔧 If Still Not Working: Nuclear Option

### Option 1: Use Blueprint Deployment

1. **Delete current service**
2. **In Render Dashboard**: Click "New +" → "Blueprint"
3. **Connect repository**
4. **Select `render.yaml`** (it's in your b2b-backend folder)
5. **Render will use the yaml configuration**
6. **Add environment variables manually** (DATABASE_URL, SECRET_KEY)

### Option 2: Deploy from Subdirectory Only

Create a new repository with ONLY the backend:

```bash
# In your local machine
cd b2b-backend
git init
git add .
git commit -m "Backend only"
git remote add origin <new-repo-url>
git push -u origin main
```

Then deploy this new repo to Render (no Root Directory needed).

### Option 3: Use Dockerfile

Create a Dockerfile deployment instead of native Python:

1. **In Render**: Create "Docker" service (not Python)
2. **Dockerfile** is already in your b2b-backend folder
3. **Render will use Docker** instead of auto-detection

---

## 🎯 Screenshot Checklist

Take screenshots of these settings to verify:

### Screenshot 1: Root Directory
- Go to: Settings → Root Directory
- Should show: `b2b-backend`
- NOT: empty or `.`

### Screenshot 2: Build Command
- Go to: Settings → Build & Deploy
- Build Command should start with: `pip install` or `chmod`
- NOT: empty or auto-detected

### Screenshot 3: Start Command
- Go to: Settings → Build & Deploy
- Start Command should be: `gunicorn app.main:app --workers 2...`
- NOT: `gunicorn b2b-backend.wsgi`

### Screenshot 4: Environment Variables
- Go to: Environment
- Should have: DISABLE_COLLECTSTATIC=1
- Should have: PYTHON_VERSION=3.11.0
- Should have: DATABASE_URL
- Should have: SECRET_KEY

---

## 🆘 Common Mistakes

### Mistake 1: Root Directory Not Set
**Symptom**: Render runs `gunicorn b2b-backend.wsgi`
**Fix**: Set Root Directory to `b2b-backend` BEFORE first deploy

### Mistake 2: Start Command Has Typo
**Symptom**: Error about module not found
**Fix**: Copy-paste the exact command from this guide

### Mistake 3: Using render.yaml Without Blueprint
**Symptom**: render.yaml is ignored
**Fix**: Either use "Blueprint" deployment OR manually configure settings

### Mistake 4: Environment Variables Not Set
**Symptom**: Build succeeds but app crashes on start
**Fix**: Add all required environment variables

---

## 📋 Final Verification Command

After deployment, run this in Render Shell (if available):

```bash
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Gunicorn version: $(gunicorn --version)"
ls -la
python -c "import app.main; print('FastAPI app found!')"
```

Should output:
```
Current directory: /opt/render/project/src/b2b-backend
Python version: Python 3.11.0
Gunicorn version: gunicorn (version 23.0.0)
FastAPI app found!
```

---

## 🎉 Success Indicators

### In Build Logs:
- ✅ "Using root directory: b2b-backend"
- ✅ "Successfully installed gunicorn-23.0.0"
- ✅ "Build succeeded"

### In Runtime Logs:
- ✅ "Starting gunicorn 23.0.0"
- ✅ "Using worker: uvicorn.workers.UvicornWorker"
- ✅ "Application startup complete"

### In Browser:
- ✅ `https://your-app.onrender.com/` returns response
- ✅ `https://your-app.onrender.com/docs` shows FastAPI docs

---

## 📞 Still Failing?

If you've tried everything and it still runs `gunicorn b2b-backend.wsgi`:

1. **Contact Render Support** - This might be a platform bug
2. **Use Docker deployment** - More reliable for complex setups
3. **Deploy backend to separate repo** - Simplest solution
4. **Try different platform** - Railway, Fly.io, or Heroku

---

**Last Resort**: Share your Render service URL and I can help debug further.

**Last Updated**: March 2026
