# 🚀 Deploy to Render NOW - Simple Steps

## ⚠️ CRITICAL: Set Root Directory First!

**In Render Dashboard → Settings → Root Directory:**
```
b2b-backend
```

This is THE MOST IMPORTANT setting for monorepo deployments!

---

## Copy-Paste These Commands in Render Dashboard

### 1. Root Directory (MUST SET FIRST!)
```
b2b-backend
```

### 2. Build Command
```bash
pip install --upgrade pip && pip install --only-binary=:all: --no-cache-dir -r requirements.txt && alembic upgrade head
```

### 3. Start Command
```bash
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
```

### 4. Environment Variables to Add

Click "Environment" tab and add these:

**Build Configuration:**
```
PYTHON_VERSION=3.11.0
PIP_PREFER_BINARY=1
PIP_ONLY_BINARY=:all:
DISABLE_COLLECTSTATIC=1
```

**Required for app to work:**
```
DATABASE_URL=<your-postgres-internal-url>
SECRET_KEY=<generate-random-string>
```

**Optional (for SMS/OTP):**
```
TWILIO_ACCOUNT_SID=<your-twilio-sid>
TWILIO_AUTH_TOKEN=<your-twilio-token>
TWILIO_PHONE_NUMBER=<your-twilio-number>
```

---

## Generate SECRET_KEY

Run this in your terminal:
```bash
openssl rand -hex 32
```

Copy the output and use it as SECRET_KEY.

---

## Where to Put These

### In Render Dashboard:

1. **Settings** → **Root Directory**
   - Type: `b2b-backend`
   - Click "Save Changes"
   - ⚠️ THIS IS CRITICAL FOR MONOREPO!

2. **Settings** → **Build & Deploy**
   - Paste Build Command
   - Paste Start Command
   - Click "Save Changes"

3. **Environment** tab
   - Click "Add Environment Variable"
   - Add each variable one by one
   - Click "Save Changes"

4. **Manual Deploy**
   - Click "Manual Deploy"
   - Select "Deploy latest commit"
   - Wait for build to complete

---

## ✅ Verify It's Working

Check deployment logs for these lines:

```
==> Using root directory: b2b-backend  ← MUST SEE THIS!
==> Installing dependencies
Successfully installed gunicorn-23.0.0 pydantic-2.9.2 ...
==> Build succeeded 🎉
==> Starting service
[INFO] Starting gunicorn 23.0.0
[INFO] Using worker: uvicorn.workers.UvicornWorker
INFO: Application startup complete.
```

---

## ❌ If You See This (WRONG):

```
==> Running 'gunicorn b2b-backend.wsgi'
ModuleNotFoundError: No module named 'b2b-backend'
```

**Fix**: Root Directory is NOT set! Go back to Settings → Root Directory → Set to `b2b-backend`

---

## ✅ That's It!

Your app should deploy successfully now.

Then visit:
- Your app: `https://your-app.onrender.com/`
- API docs: `https://your-app.onrender.com/docs`

---

## 🆘 Need More Help?

- **Monorepo issues**: Read `RENDER_MONOREPO_FIX.md`
- **Build errors**: Read `QUICK_FIX.md`
- **Complete guide**: Read `RENDER_DEPLOYMENT.md`
