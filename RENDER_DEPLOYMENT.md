# Deploy B2B Backend to Render

## Quick Fix for Current Error

The error you're seeing is because pydantic-core is trying to compile Rust code on Render's read-only filesystem. Here's how to fix it:

### Solution 1: Use Updated requirements.txt (RECOMMENDED)

The `requirements.txt` has been updated with:
- Newer pydantic versions (2.9.2) with pre-built wheels
- Explicit pydantic-core version (2.23.4)
- Updated FastAPI and other dependencies

**Just redeploy and it should work!**

---

## Deployment Options

### Option A: Using render.yaml (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment config"
   git push
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`
   - Click "Apply"

3. **Set Environment Variables** (in Render Dashboard)
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   SECRET_KEY=your-secret-key-here
   TWILIO_ACCOUNT_SID=your-twilio-sid
   TWILIO_AUTH_TOKEN=your-twilio-token
   TWILIO_PHONE_NUMBER=your-twilio-number
   ```

### Option B: Manual Setup

1. **Create Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select `b2b-backend` folder (if monorepo)

2. **Configure Build Settings**
   - **Name**: b2b-backend
   - **Runtime**: Python 3
   - **Build Command**: 
     ```bash
     pip install --upgrade pip && pip install --only-binary=:all: -r requirements.txt && alembic upgrade head
     ```
   - **Start Command**: 
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

3. **Environment Variables**
   Add these in the "Environment" tab:
   ```
   PYTHON_VERSION=3.11.0
   PIP_PREFER_BINARY=1
   PIP_ONLY_BINARY=:all:
   DATABASE_URL=postgresql://...
   SECRET_KEY=...
   TWILIO_ACCOUNT_SID=...
   TWILIO_AUTH_TOKEN=...
   TWILIO_PHONE_NUMBER=...
   ```

4. **Create PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: b2b-database
   - Plan: Free
   - Copy the "Internal Database URL"
   - Add it as `DATABASE_URL` in your web service

---

## Important Notes

### Python Version
- Using Python 3.11.0 (specified in `runtime.txt`)
- Render supports 3.8, 3.9, 3.10, 3.11, 3.12

### Binary-Only Installation
The key to avoiding Rust compilation errors:
```bash
pip install --only-binary=:all: -r requirements.txt
```

This forces pip to use pre-built wheels only.

### Database Migrations
Migrations run automatically during build via `build.sh` or build command.

### Health Check
The app has a health check endpoint at `/` (root).

---

## Troubleshooting

### Error: "Read-only file system"
**Cause**: Trying to compile Rust code (pydantic-core)
**Fix**: Use `--only-binary=:all:` flag (already in config)

### Error: "Python version mismatch"
**Cause**: Render using wrong Python version
**Fix**: Add `runtime.txt` with `python-3.11.0` (already created)

### Error: "Module not found"
**Cause**: Dependencies not installed
**Fix**: Check build logs, ensure requirements.txt is correct

### Error: "Database connection failed"
**Cause**: DATABASE_URL not set or incorrect
**Fix**: 
1. Create PostgreSQL database in Render
2. Copy "Internal Database URL"
3. Set as `DATABASE_URL` environment variable

### Error: "Port already in use"
**Cause**: Not using Render's $PORT variable
**Fix**: Start command uses `--port $PORT` (already configured)

---

## Environment Variables Reference

### Required
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (generate with `openssl rand -hex 32`)

### Optional (for SMS/OTP)
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `TWILIO_PHONE_NUMBER` - Twilio phone number

### Build Optimization
- `PYTHON_VERSION=3.11.0`
- `PIP_PREFER_BINARY=1`
- `PIP_ONLY_BINARY=:all:`
- `PIP_NO_BUILD_ISOLATION=false`

---

## Testing Deployment

After deployment, test these endpoints:

1. **Health Check**
   ```bash
   curl https://your-app.onrender.com/
   ```

2. **API Docs**
   ```
   https://your-app.onrender.com/docs
   ```

3. **Database Connection**
   Check logs for "Database connected successfully"

---

## Free Tier Limitations

Render Free Tier:
- ✅ 750 hours/month (enough for 1 service)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Spins down after 15 min inactivity
- ⚠️ Cold start takes 30-60 seconds

PostgreSQL Free Tier:
- ✅ 1 GB storage
- ✅ 90 days retention
- ⚠️ Expires after 90 days (backup data!)

---

## Production Checklist

Before going live:

- [ ] Set strong `SECRET_KEY`
- [ ] Configure CORS origins in `app/main.py`
- [ ] Set up database backups
- [ ] Configure custom domain
- [ ] Set up monitoring/alerts
- [ ] Test all API endpoints
- [ ] Verify Firebase authentication works
- [ ] Test OTP/SMS functionality
- [ ] Check database migrations applied

---

## Useful Commands

### View Logs
```bash
# In Render Dashboard → Your Service → Logs
```

### Manual Migration
```bash
# In Render Shell
alembic upgrade head
```

### Check Python Version
```bash
python --version
```

### List Installed Packages
```bash
pip list
```

---

## Support

If you still encounter issues:

1. Check Render build logs
2. Check runtime logs
3. Verify environment variables
4. Test database connection
5. Check [Render Status](https://status.render.com/)

---

**Last Updated**: March 2026
**Render Docs**: https://render.com/docs
