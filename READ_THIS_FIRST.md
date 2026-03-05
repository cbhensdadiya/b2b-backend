# ⚠️ READ THIS FIRST - Fix "Could not import module 'main'" Error

## The Problem

You're getting this error:
```
ERROR: Error loading ASGI app. Could not import module "main".
```

This happens because you're running the command from the WRONG directory or using the WRONG command.

---

## ✅ THE FIX (Choose One)

### Option 1: Use the Batch Script (EASIEST)

1. Open File Explorer
2. Navigate to: `C:\CP\BVSS\trading-v1\b2b-backend\`
3. Double-click: `START_SERVER.bat`

Done! The server will start automatically.

---

### Option 2: Manual Commands (PowerShell/CMD)

```powershell
# Step 1: Navigate to b2b-backend directory
cd C:\CP\BVSS\trading-v1\b2b-backend

# Step 2: Activate virtual environment
.\venv\Scripts\activate

# Step 3: Start server with CORRECT command
uvicorn app.main:app --reload
```

**IMPORTANT**: Use `app.main:app` NOT `main:app`

---

## 🚫 Common Mistakes

### ❌ WRONG - Running from wrong directory:
```powershell
C:\CP\BVSS\trading-v1> uvicorn app.main:app --reload
# ERROR: You're in trading-v1, not b2b-backend!
```

### ❌ WRONG - Using wrong module path:
```powershell
C:\CP\BVSS\trading-v1\b2b-backend> uvicorn main:app --reload
# ERROR: Should be "app.main:app" not "main:app"
```

### ✅ CORRECT:
```powershell
C:\CP\BVSS\trading-v1\b2b-backend> uvicorn app.main:app --reload
# SUCCESS: Correct directory + correct command
```

---

## 🎯 Quick Reference

### Correct Directory:
```
C:\CP\BVSS\trading-v1\b2b-backend
```

### Correct Command:
```powershell
uvicorn app.main:app --reload
```

### Full Command Sequence:
```powershell
cd C:\CP\BVSS\trading-v1\b2b-backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

---

## 🧪 Test If You're in the Right Place

Run this command:
```powershell
python test_import.py
```

Should output:
```
✅ SUCCESS: app.main imported successfully!
```

If you see an error, you're in the wrong directory!

---

## 📋 Step-by-Step Visual Guide

### Step 1: Check Your Current Directory
```powershell
PS C:\CP\BVSS\trading-v1> pwd
```

If you see `trading-v1`, you need to go into `b2b-backend`:
```powershell
PS C:\CP\BVSS\trading-v1> cd b2b-backend
PS C:\CP\BVSS\trading-v1\b2b-backend>  # ← Now you're in the right place!
```

### Step 2: Verify Files Exist
```powershell
PS C:\CP\BVSS\trading-v1\b2b-backend> dir app
```

Should show:
- main.py
- api/
- core/
- models/
- schemas/

### Step 3: Activate Virtual Environment
```powershell
PS C:\CP\BVSS\trading-v1\b2b-backend> .\venv\Scripts\activate
(venv) PS C:\CP\BVSS\trading-v1\b2b-backend>  # ← (venv) prefix appears
```

### Step 4: Start Server
```powershell
(venv) PS C:\CP\BVSS\trading-v1\b2b-backend> uvicorn app.main:app --reload
```

Should output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## 🎉 Success Indicators

When it works, you'll see:
```
INFO:     Will watch for changes in these directories: ['C:\\CP\\BVSS\\trading-v1\\b2b-backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then visit: http://localhost:8000/docs

---

## 🆘 Still Not Working?

### Check 1: Are you in the right directory?
```powershell
pwd
# Should show: C:\CP\BVSS\trading-v1\b2b-backend
```

### Check 2: Does app/main.py exist?
```powershell
Test-Path app\main.py
# Should show: True
```

### Check 3: Is venv activated?
```powershell
# Your prompt should show (venv) at the start:
(venv) PS C:\CP\BVSS\trading-v1\b2b-backend>
```

### Check 4: Test the import
```powershell
python -c "import app.main; print('OK')"
# Should print: OK
```

If any of these fail, you're not in the right directory or venv is not activated!

---

## 📞 Quick Help

**Problem**: "Could not import module 'main'"
**Solution**: Use `app.main:app` not `main:app`

**Problem**: "No module named 'app'"
**Solution**: You're in the wrong directory. Go to `b2b-backend`

**Problem**: "No module named 'src'"
**Solution**: You're in the wrong directory. Go to `b2b-backend`

---

## 🎯 The Golden Rule

**ALWAYS run commands from the `b2b-backend` directory!**

```
✅ C:\CP\BVSS\trading-v1\b2b-backend>
❌ C:\CP\BVSS\trading-v1>
❌ C:\CP\BVSS>
❌ C:\CP>
```

---

**Last Updated**: March 2026
