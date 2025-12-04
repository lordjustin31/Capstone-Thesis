"""
Django settings for core project.
"""

from pathlib import Path
from datetime import timedelta
import os
import secrets
import dj_database_url
import warnings

# ---------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# DEBUG MODE
# ---------------------------------------------------------
DEBUG_ENV = os.environ.get("DEBUG", "").lower()

if DEBUG_ENV == "false":
    DEBUG = False
elif DEBUG_ENV == "true":
    DEBUG = True
else:
    # Default: True locally, False on Render
    DEBUG = "RENDER" not in os.environ

# ---------------------------------------------------------
# SECRET KEY
# ---------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        # Local development: use insecure fallback
        SECRET_KEY = "django-insecure-dev-key-only-for-local-development-change-in-production"
        warnings.warn(
            "WARNING: SECRET_KEY not set! Using insecure development key.",
            UserWarning
        )
    else:
        # Production: generate a stable secret key based on service identifier
        # Check if we're on Render (check multiple indicators)
        is_render = (
            "RENDER" in os.environ or 
            "RENDER_SERVICE_NAME" in os.environ or
            os.environ.get("HOSTNAME", "").endswith(".onrender.com") or
            os.environ.get("DATABASE_URL", "").startswith("postgresql://")
        )
        
        # Generate a stable secret key based on service name or hostname
        # This ensures the same key is used across restarts
        service_id = (
            os.environ.get("RENDER_SERVICE_NAME") or 
            os.environ.get("HOSTNAME", "default-service") or 
            "default-service"
        )
        
        # Use a deterministic but secure method to generate key
        import hashlib
        seed = f"{service_id}-happy-homes-secret-key-seed-2024"
        hash_obj = hashlib.sha256(seed.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Convert to Django-compatible secret key format
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)'
        SECRET_KEY = ''.join(chars[int(hash_hex[i:i+2], 16) % len(chars)] for i in range(0, min(100, len(hash_hex)), 2))[:50]
        
        if is_render:
            warnings.warn(
                "WARNING: SECRET_KEY not set in environment! Generated a stable one based on service. "
                "Set SECRET_KEY in Render dashboard for better security and consistency.",
                UserWarning
            )
        else:
            warnings.warn(
                "WARNING: SECRET_KEY not set in environment! Generated a stable one. "
                "Set SECRET_KEY environment variable for production use.",
                UserWarning
            )

# ---------------------------------------------------------
# ALLOWED HOSTS
# ---------------------------------------------------------
# Check for ALLOW_ALL_HOSTS (from render.yaml) or ALLOWED_HOSTS
ALLOW_ALL_HOSTS = os.environ.get("ALLOW_ALL_HOSTS", "False").lower() == "true"
ALLOWED_HOSTS_ENV = os.environ.get("ALLOWED_HOSTS", "").strip()

if ALLOW_ALL_HOSTS:
    # Allow all hosts (for Render or when explicitly enabled)
    ALLOWED_HOSTS = ["*"]
elif ALLOWED_HOSTS_ENV:
    # Use explicitly set hosts
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(",") if host.strip()]
else:
    # Default settings
    if DEBUG:
        ALLOWED_HOSTS = ["*"]
    else:
        # Production: allow all hosts (Render handles routing)
        # For better security, set ALLOWED_HOSTS env var with specific domains
        ALLOWED_HOSTS = ["*"]

# ---------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "simple_history",
    "corsheaders",

    # Local apps
    "api",
    "core",
]

# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "core.urls"

# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------
# REST FRAMEWORK
# ---------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
}

# ---------------------------------------------------------
# JWT SETTINGS
# ---------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# ---------------------------------------------------------
# CORS & CSRF
# ---------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = os.environ.get("CORS_ALLOW_ALL_ORIGINS", "False").lower() == "true"
CORS_ALLOW_CREDENTIALS = True

# CORS allowed origins
CORS_ALLOWED_ORIGINS_ENV = os.environ.get("CORS_ALLOWED_ORIGINS", "").strip()
if CORS_ALLOWED_ORIGINS_ENV:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_ENV.split(",") if origin.strip()]
else:
    # Default: allow localhost and Render domains
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://capstone-thesis-w018.onrender.com",
    ]
    
    # If ALLOW_ALL_HOSTS is True, also allow all CORS origins
    if ALLOW_ALL_HOSTS:
        CORS_ALLOW_ALL_ORIGINS = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS_ENV = os.environ.get("CSRF_TRUSTED_ORIGINS", "").strip()
if CSRF_TRUSTED_ORIGINS_ENV:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS_ENV.split(",") if origin.strip()]
else:
    # Default: allow localhost and Render domains
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://capstone-thesis-w018.onrender.com",
        "https://*.onrender.com",  # Note: Django doesn't support wildcards, but keeping for reference
    ]
    # Remove wildcard and add common Render pattern
    CSRF_TRUSTED_ORIGINS = [origin for origin in CSRF_TRUSTED_ORIGINS if not origin.endswith("*")]

# ---------------------------------------------------------
# EMAIL
# ---------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "1") == "1"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "happyphhomes@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", f"Happy Homes <{EMAIL_HOST_USER}>")

# ---------------------------------------------------------
# FRONTEND URL
# ---------------------------------------------------------
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://caps-rouge.vercel.app")

# ---------------------------------------------------------
# PRODUCTION SECURITY HEADERS
# ---------------------------------------------------------
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    X_FRAME_OPTIONS = "DENY"

# ---------------------------------------------------------
# FILE STORAGE (S3 or Local)
# ---------------------------------------------------------
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")
    AWS_QUERYSTRING_AUTH = False
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
