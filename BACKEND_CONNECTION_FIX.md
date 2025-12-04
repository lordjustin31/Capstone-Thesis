# Backend Connection Fix

## Problem
Frontend cannot connect to backend at `https://capstone-thesis-w018.onrender.com`

## Root Causes

1. **Render Free Tier Sleep**: Render free tier services sleep after 15 minutes of inactivity. The first request after sleeping takes 30-60 seconds to wake up the service.

2. **CORS Configuration**: CORS settings needed to properly allow all origins when `CORS_ALLOW_ALL_ORIGINS = True`.

3. **Timeout Issues**: Frontend requests were timing out before the backend could wake up.

## Fixes Applied

### 1. CORS Configuration (`backend/core/settings.py`)
- Fixed CORS logic to properly respect `CORS_ALLOW_ALL_ORIGINS = True`
- When `CORS_ALLOW_ALL_ORIGINS` is True, all origins are allowed regardless of `CORS_ALLOWED_ORIGINS` list
- Added automatic Vercel URL detection from `FRONTEND_URL` environment variable
- Added localhost ports 3000 and 8000 to default allowed origins

### 2. Frontend Retry Logic (`frontend/my-app/src/pages/LoginPage.tsx`)
- Added `fetchWithRetry` function that retries failed requests up to 2 times
- Increased timeout to 90 seconds to accommodate Render's wake-up time
- Added 2-second delay between retries
- Improved error messages to inform users about Render's sleeping behavior

### 3. Error Messages
- Updated error messages to explain that the server may be sleeping
- Added helpful information about wait times

## Testing

1. **First Request After Sleep**:
   - Wait 30-60 seconds for the first request
   - The retry mechanism will automatically handle this

2. **Subsequent Requests**:
   - Should be fast (normal response time)

3. **If Still Failing**:
   - Check Render dashboard logs for errors
   - Verify environment variables are set correctly
   - Check that the backend service is running (not suspended)

## Environment Variables (Render Dashboard)

Ensure these are set in Render:
- `CORS_ALLOW_ALL_ORIGINS`: `True`
- `ALLOW_ALL_HOSTS`: `True`
- `FRONTEND_URL`: Your Vercel frontend URL (e.g., `https://your-app.vercel.app`)

## Next Steps

1. **Commit and Push**:
   ```bash
   git add backend/core/settings.py frontend/my-app/src/pages/LoginPage.tsx
   git commit -m "Fix CORS configuration and add retry logic for Render sleeping services"
   git push origin main
   ```

2. **Wait for Deployment**:
   - Render will auto-deploy the backend
   - Vercel will auto-deploy the frontend

3. **Test Login**:
   - First login after deployment may take 30-60 seconds (waking up)
   - Subsequent logins should be fast

## Alternative Solutions

If the sleeping behavior is problematic:

1. **Upgrade Render Plan**: Paid plans don't sleep
2. **Use a Keep-Alive Service**: Services like UptimeRobot can ping your backend every 5 minutes
3. **Move to Different Hosting**: Consider Railway, Fly.io, or other services with better free tier

## Verification

To verify the backend is working:
1. Visit `https://capstone-thesis-w018.onrender.com/api/token/` in browser
2. Should see a response (even if it's an error, it means the server is running)
3. Check Render dashboard logs for any errors

