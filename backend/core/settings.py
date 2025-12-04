"""
Django settings for core project.
"""

from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

# --- Base directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
# DEBUG defaults to True for local development
# Set DEBUG=False in production via environment variable
DEBUG_ENV = os.environ.get("DEBUG", "").lower()
if DEBUG_ENV == "false":
    DEBUG = False
elif DEBUG_ENV == "true":
    DEBUG = True
else:
    # Default to True for local development if not explicitly set
    # Check if we're likely in production (Render sets RENDER env var)
    DEBUG = "RENDER" not in os.environ

# SECRET_KEY must be set via environment variable in production
# For local development, a fallback key is provided (NEVER use in production!)
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        # Development-only fallback key - DO NOT use in production!
        SECRET_KEY = "django-insecure-dev-key-only-for-local-development-change-in-production"
        import warnings
        warnings.warn(
            "SECRET_KEY not set! Using development fallback. "
            "Set SECRET_KEY environment variable for production.",
            UserWarning
        )
    else:
        raise ValueError(
            "SECRET_KEY environment variable is required in production! "
            "Set it in your environment variables."
        )

# ALLOWED_HOSTS - for production, set specific domains
# For Render: use your Render service URL or set via environment variable
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",") if os.environ.get("ALLOWED_HOSTS") else ["*"]

# --- Applications ---
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "simple_history",
    

    # Local apps
    "api",
    "core",
]

# Allow CORS
INSTALLED_APPS += [
    'corsheaders',
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",           # Security headers
    "whitenoise.middleware.WhiteNoiseMiddleware",             # Static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

# Insert CORS middleware at the beginning
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

ROOT_URLCONF = "core.urls"

# --- Templates ---
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

# --- Database ---
# Uses PostgreSQL on Render (via DATABASE_URL env var) or SQLite for local development
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    # Production: Use PostgreSQL from DATABASE_URL
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL)
    }
else:
    # Development: Use SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- Password validators ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalization ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Production
# Only include static directory if it exists (to avoid warnings)
static_dir = BASE_DIR / "static"
STATICFILES_DIRS = [static_dir] if static_dir.exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- REST Framework ---
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

# --- JWT settings ---
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# --- CORS & CSRF ---
# CORS configuration - for production, set specific origins
CORS_ALLOW_ALL_ORIGINS = os.environ.get("CORS_ALLOW_ALL_ORIGINS", "False").lower() == "true"
CORS_ALLOW_CREDENTIALS = True

# Get allowed origins from environment or use defaults
CORS_ALLOWED_ORIGINS_ENV = os.environ.get("CORS_ALLOWED_ORIGINS", "")
if CORS_ALLOWED_ORIGINS_ENV:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_ENV.split(",")]
else:
    # Default origins (development)
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS_ENV = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if CSRF_TRUSTED_ORIGINS_ENV:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS_ENV.split(",")]
else:
    # Default origins (development)
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

# --- Email ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "1") == "1"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "happyphhomes@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", f"Happy Homes <{EMAIL_HOST_USER}>")
CONTACT_INBOX_EMAIL = os.environ.get("CONTACT_INBOX_EMAIL", DEFAULT_FROM_EMAIL)

# --- Frontend URL ---
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://caps-rouge.vercel.app")

# --- Security headers for production ---
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# --- File Storage ---
# Use S3 only if AWS credentials are provided, otherwise use local storage
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    # Use S3 for production
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")
    AWS_QUERYSTRING_AUTH = False
else:
    # Use local file storage (default)
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"