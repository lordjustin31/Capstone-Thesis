# 📦 Migrate Local Media Files to Cloud Storage

## 🎯 Goal
Transfer your local media files (`backend/media/`) to cloud storage so they persist on Render and won't be lost on redeploy/restart.

---

## 🚀 Option 1: AWS S3 (Recommended for Production)

### Step 1: Create AWS S3 Bucket

1. Go to [AWS Console](https://console.aws.amazon.com/s3/)
2. Click **"Create bucket"**
3. Configure:
   - **Bucket name**: `happy-homes-media` (or your choice)
   - **Region**: `us-east-1` (or your preferred region)
   - **Block Public Access**: Uncheck (or configure CORS properly)
4. Click **"Create bucket"**

### Step 2: Create IAM User for S3 Access

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Click **"Users"** → **"Create user"**
3. Name: `happy-homes-s3-user`
4. Select **"Attach policies directly"**
5. Add policy: `AmazonS3FullAccess` (or create custom policy with only your bucket)
6. Click **"Create user"**
7. Go to **"Security credentials"** tab
8. Click **"Create access key"**
9. Choose **"Application running outside AWS"**
10. **Save the Access Key ID and Secret Access Key** (you'll need these)

### Step 3: Install Required Packages

Add to `backend/requirements.txt`:
```
django-storages
boto3
```

Then install:
```bash
cd backend
pip install django-storages boto3
```

### Step 4: Update Settings

Your `settings.py` already has S3 configuration! Just add these environment variables in Render:

```
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_STORAGE_BUCKET_NAME=happy-homes-media
AWS_S3_REGION_NAME=us-east-1
```

### Step 5: Upload Existing Files

Run the migration script:
```bash
cd backend
python upload_media_to_cloud.py
```

This will upload all your local media files to S3.

---

## 🌟 Option 2: Cloudinary (Easier Setup)

### Step 1: Sign Up for Cloudinary

1. Go to [Cloudinary](https://cloudinary.com/users/register/free)
2. Sign up for free account
3. Go to **Dashboard** → Copy your credentials:
   - Cloud Name
   - API Key
   - API Secret

### Step 2: Install Package

Add to `backend/requirements.txt`:
```
django-cloudinary-storage
cloudinary
```

Install:
```bash
cd backend
pip install django-cloudinary-storage cloudinary
```

### Step 3: Update Settings

Add to `backend/core/settings.py` in `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... existing apps
    'cloudinary_storage',  # Add this
    'django.contrib.staticfiles',
    # ... rest of apps
]
```

Add to settings:
```python
# Cloudinary settings
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
```

### Step 4: Set Environment Variables in Render

```
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Step 5: Upload Existing Files

Run the migration script:
```bash
cd backend
python upload_media_to_cloud.py
```

---

## 📋 Quick Comparison

| Feature | AWS S3 | Cloudinary |
|---------|--------|------------|
| **Setup Difficulty** | Medium | Easy |
| **Cost** | Pay per use (~$0.023/GB) | Free tier: 25GB |
| **Image Optimization** | Manual | Automatic |
| **Best For** | Production, large scale | Quick setup, image-heavy apps |

---

## ✅ After Migration

1. **Test locally** with cloud storage configured
2. **Deploy to Render** with environment variables set
3. **Verify files** are accessible at your media URLs
4. **Delete local media files** (optional, after confirming cloud storage works)

---

## 🔄 Database Migration

**Important**: Your database records reference file paths. After migrating to cloud storage:

- ✅ **Existing records**: Will automatically use cloud URLs (Django handles this)
- ✅ **New uploads**: Will go directly to cloud storage
- ⚠️ **Old file paths**: May need updating if you change storage backend

---

## 🎯 Recommended Approach

1. **For now (testing)**: Keep local storage, test deployment
2. **For production**: Set up AWS S3 or Cloudinary
3. **Run migration script**: Upload all existing files
4. **Update Render**: Add cloud storage environment variables
5. **Redeploy**: Files will now persist!

---

## 💡 Tips

- **Test locally first** before deploying
- **Keep local backup** until you verify cloud storage works
- **Monitor usage** on cloud storage dashboard
- **Set up CORS** properly for S3 if needed
- **Use CloudFront** (AWS CDN) for faster file delivery (optional)

