"""
Script to upload existing local media files to cloud storage (AWS S3 or Cloudinary)
Run this script once to migrate your local media files to cloud storage.

Usage:
    python upload_media_to_cloud.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.files.storage import default_storage
from django.conf import settings

def upload_media_files():
    """Upload all media files from local storage to cloud storage"""
    media_root = Path(settings.MEDIA_ROOT)
    
    if not media_root.exists():
        print(f"Media directory not found: {media_root}")
        return
    
    print(f"Starting upload from: {media_root}")
    print(f"Storage backend: {settings.DEFAULT_FILE_STORAGE}")
    print("-" * 50)
    
    uploaded_count = 0
    skipped_count = 0
    error_count = 0
    
    # Walk through all files in media directory
    for root, dirs, files in os.walk(media_root):
        for file in files:
            file_path = Path(root) / file
            
            # Get relative path from media root
            relative_path = file_path.relative_to(media_root)
            relative_path_str = str(relative_path).replace('\\', '/')  # Normalize path
            
            try:
                # Check if file already exists in cloud storage
                if default_storage.exists(relative_path_str):
                    print(f"⏭️  Skipped (exists): {relative_path_str}")
                    skipped_count += 1
                    continue
                
                # Read and upload file
                with open(file_path, 'rb') as f:
                    default_storage.save(relative_path_str, f)
                
                print(f"✅ Uploaded: {relative_path_str}")
                uploaded_count += 1
                
            except Exception as e:
                print(f"❌ Error uploading {relative_path_str}: {str(e)}")
                error_count += 1
    
    print("-" * 50)
    print(f"Upload complete!")
    print(f"  ✅ Uploaded: {uploaded_count} files")
    print(f"  ⏭️  Skipped: {skipped_count} files")
    print(f"  ❌ Errors: {error_count} files")

if __name__ == '__main__':
    # Check if cloud storage is configured
    if 's3' in settings.DEFAULT_FILE_STORAGE.lower():
        print("Using AWS S3 storage")
        if not all([
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
            settings.AWS_STORAGE_BUCKET_NAME
        ]):
            print("❌ AWS credentials not configured!")
            print("Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_STORAGE_BUCKET_NAME")
            sys.exit(1)
    elif 'cloudinary' in settings.DEFAULT_FILE_STORAGE.lower():
        print("Using Cloudinary storage")
    else:
        print("⚠️  Warning: Using local file storage")
        print("Files will not persist on Render free tier")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    upload_media_files()

