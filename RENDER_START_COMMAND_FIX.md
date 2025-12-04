# 🔧 Fix Render Start Command Error

## ❌ Current Error
```
ModuleNotFoundError: No module named 'your_application'
==> Running 'gunicorn your_application.wsgi'
```

## ✅ Solution: Update Start Command in Render Dashboard

Render is using an old Start Command from the dashboard settings. You need to update it manually.

### Step 1: Go to Render Dashboard

1. Open [Render Dashboard](https://dashboard.render.com)
2. Click on your **Web Service** (happy-homes-backend)
3. Go to **Settings** tab
4. Scroll down to **Start Command**

### Step 2: Update Start Command

**Find this field:**
```
Start Command
```

**Replace the current value (if it says):**
```
gunicorn your_application.wsgi
```

**With this correct command:**
```
cd backend && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 3: Save and Redeploy

1. Click **Save Changes**
2. Render will automatically redeploy
3. The error should be fixed!

---

## ✅ Alternative: Use Procfile (Recommended)

If you want Render to automatically use the Procfile:

1. Go to **Settings** → **Start Command**
2. **Clear/Delete** the Start Command field (leave it empty)
3. Make sure **Procfile** is in your repository root
4. Render will automatically detect and use it

**Your Procfile contains:**
```
web: cd backend && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 📋 Correct Commands Reference

### If Root Directory is Project Root (default):
```
cd backend && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

### If Root Directory is set to `backend`:
```
python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

---

## ✅ Verification

After updating, check the logs. You should see:
```
==> Running 'cd backend && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT'
```

**NOT:**
```
==> Running 'gunicorn your_application.wsgi'  ❌
```

---

## 🎯 Quick Fix Checklist

- [ ] Go to Render Dashboard → Your Service → Settings
- [ ] Find "Start Command" field
- [ ] Replace with: `cd backend && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`
- [ ] Save Changes
- [ ] Wait for redeploy
- [ ] Check logs - should see `core.wsgi:application` not `your_application.wsgi`

---

## 💡 Why This Happened

Render dashboard settings override:
- Procfile
- render.yaml startCommand

You must update the dashboard manually if it has an old value stored.

