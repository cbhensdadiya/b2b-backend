# 🚀 Deploy to Render NOW - Simple Steps

## Copy-Paste These Commands in Render Dashboard

### 1. Build Command
```bash
pip install --upgrade pip && pip install --only-binary=:all: --no-cache-dir -r requirements.txt && alembic upgrade head
```

### 2. Start Command
```bash
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 3. Environment Variables to Add

Click "Environment" tab and add these:

```
PYTHON_VERSION=3.11.0
PIP_PREFER_BINARY=1
PIP_ONLY_BINARY=:all:
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

1. **Go to your service**
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

## ✅ That's It!

Your app should deploy successfully now.

Check logs for:
```
[INFO] Application startup complete.
```

Then visit:
- Your app: `https://your-app.onrender.com/`
- API docs: `https://your-app.onrender.com/docs`
