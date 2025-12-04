# 🚀 Render Deployment Checklist - Happy Homes

## ✅ Pre-Deployment Security Fixes (COMPLETED)

### 1. ✅ SECRET_KEY - FIXED
- ❌ **Before**: Hardcoded in settings.py
- ✅ **After**: Must be set via `SECRET_KEY` environment variable
- **Action Required**: Generate and set `SECRET_KEY` in Render dashboard

### 2. ✅ DEBUG - FIXED
- ❌ **Before**: Could be True in production
- ✅ **After**: Defaults to `False`, only `True` if explicitly set
- **Action Required**: Ensure `DEBUG=False` in Render environment variables

### 3. ✅ ALLOWED_HOSTS - FIXED
- ❌ **Before**: Had ngrok URLs that expire
- ✅ **After**: Configurable via environment variable, defaults to `['*']`
- **Action Required**: Set specific domains in Render after deployment

### 4. ✅ CORS - FIXED
- ❌ **Before**: Hardcoded local/ngrok URLs
- ✅ **After**: Configurable via environment variables
- **Action Required**: Set `CORS_ALLOWED_ORIGINS` with your frontend URL

### 5. ✅ Database - FIXED
- ❌ **Before**: SQLite (not allowed in production)
- ✅ **After**: Uses PostgreSQL via `DATABASE_URL` (auto-set by Render)
- **Action Required**: None - Render automatically provides `DATABASE_URL`

### 6. ✅ EMAIL Password - FIXED
- ❌ **Before**: Hardcoded in settings.py
- ✅ **After**: Must be set via `EMAIL_HOST_PASSWORD` environment variable
- **Action Required**: Set Gmail app password in Render dashboard

### 7. ✅ Non-Production Files - FIXED
- ❌ **Before**: Debug scripts, .bat, .ps1 files committed
- ✅ **After**: Added to .gitignore
- **Action Required**: None - files are now ignored

---

## 📋 Render Deployment Steps

### Step 1: Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **PostgreSQL**
3. Configure:
   - **Name**: `happy-homes-db`
   - **Database**: `happy_homes`
   - **User**: `happy_homes_user` (or auto-generated)
   - **Region**: Choose closest to you
4. Click **Create Database**
5. **Note the connection string** - Render will auto-set `DATABASE_URL`

### Step 2: Create Web Service (Backend)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `happy-homes-backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     cd backend && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Root Directory**: Leave empty (or set to `backend`)

### Step 3: Set Environment Variables in Render

Go to your Web Service → **Environment** tab and add:

#### Required Variables:

```bash
# SECRET_KEY - Generate a new one!
SECRET_KEY=your-generated-secret-key-here

# DEBUG - Must be False for production
DEBUG=False

# Database - Auto-set by Render if you link the PostgreSQL service
# DATABASE_URL=postgresql://... (automatically set)

# Allowed Hosts - Use your Render service URL
ALLOWED_HOSTS=happy-homes-backend.onrender.com

# CORS - Set your frontend URL
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=happyphhomes@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password-here
DEFAULT_FROM_EMAIL=Happy Homes <happyphhomes@gmail.com>
CONTACT_INBOX_EMAIL=happyphhomes@gmail.com

# Frontend URL
FRONTEND_URL=https://your-frontend.vercel.app
```

#### Optional (for AWS S3 media storage):

```bash
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Step 4: Link PostgreSQL Database

1. In your Web Service settings
2. Go to **Environment** tab
3. Find **Add Environment Variable** → **Link Database**
4. Select your PostgreSQL database
5. Render will automatically set `DATABASE_URL`

### Step 5: Deploy

1. Click **Save Changes**
2. Render will automatically:
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start the server

### Step 6: Verify Deployment

1. Check logs for any errors
2. Visit your service URL: `https://happy-homes-backend.onrender.com`
3. Test API endpoints
4. Verify database connection

---

## 🔐 Generate SECRET_KEY

Run this command locally to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use Django shell:

```bash
cd backend
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
```

Copy the output and use it as your `SECRET_KEY` in Render.

---

## 📝 Post-Deployment Checklist

- [ ] Backend service is running
- [ ] Database migrations completed successfully
- [ ] Static files collected
- [ ] API endpoints responding
- [ ] CORS working (test from frontend)
- [ ] Email sending works (test password reset)
- [ ] Media uploads working (if using S3)
- [ ] All environment variables set correctly
- [ ] DEBUG=False confirmed
- [ ] SECRET_KEY is not in code (check GitHub)

---

## 🆘 Troubleshooting

### Database Connection Error
- Verify `DATABASE_URL` is set in environment variables
- Check PostgreSQL service is running
- Verify database credentials

### Static Files Not Loading
- Check `collectstatic` ran successfully in build logs
- Verify `STATIC_ROOT` is set correctly
- Check WhiteNoise middleware is in MIDDLEWARE

### CORS Errors
- Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
- Check `CORS_ALLOW_ALL_ORIGINS` is False in production
- Ensure CORS middleware is first in MIDDLEWARE list

### 500 Internal Server Error
- Check logs in Render dashboard
- Verify all environment variables are set
- Check SECRET_KEY is set
- Verify DEBUG=False

---

## ✅ Security Verification

Before going live, verify:

1. ✅ No hardcoded secrets in code
2. ✅ DEBUG=False in production
3. ✅ SECRET_KEY is from environment variable
4. ✅ Database uses PostgreSQL (not SQLite)
5. ✅ CORS configured for specific origins
6. ✅ Email password not in code
7. ✅ All sensitive files in .gitignore

---

## 🎉 You're Ready!

Your Django backend is now production-ready and secure for Render deployment!

