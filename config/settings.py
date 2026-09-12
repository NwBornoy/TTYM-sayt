"""
Qashqadaryo TTY sayti — Django sozlamalari.

XAVFSIZLIK BO'YICHA ASOSIY QOIDALAR:
- SECRET_KEY va boshqa maxfiy qiymatlar HECH QACHON kodga yozilmaydi — .env orqali o'qiladi.
- Production'da DEBUG=False bo'lishi SHART. DEBUG=True xatolik sahifalarida
  server manzillari, sozlamalar va hatto SECRET_KEY sizib chiqishiga olib kelishi mumkin.
- ALLOWED_HOSTS aniq domenlar bilan cheklanadi.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # .env faylini o'qiydi (agar mavjud bo'lsa)

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Maxfiy sozlamalar (.env orqali) -----------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "faqat-lokal-sinov-uchun-secret-key-buni-production-da-ishlatmang",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()
]

# --- Ilovalar ------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_ckeditor_5",
    "blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",       # CSRF himoyasi — barcha formalarda kerak
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # clickjacking'dan himoya
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# --- Ma'lumotlar bazasi ---------------------------------------------------
# Sinov uchun SQLite, production uchun DATABASE_URL orqali PostgreSQL tavsiya etiladi.
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url  # pip install dj-database-url (agar postgres ishlatsangiz)
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- Parollarni tekshirish (kuchsiz parollarning oldini oladi) -----------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "blog.validators.UzbekUserAttributeSimilarityValidator"},
    {"NAME": "blog.validators.UzbekMinimumLengthValidator", "OPTIONS": {"min_length": 7}},
    {"NAME": "blog.validators.UzbekCommonPasswordValidator"},
    {"NAME": "blog.validators.UzbekNumericPasswordValidator"},
]

LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [BASE_DIR / "blog" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"   # `collectstatic` shu yerga yig'adi

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# --- CKEditor 5 sozlamalari --------------------------------------------------
CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'underline', '|',
                    'bulletedList', 'numberedList', '|',
                    'link', 'blockQuote', 'imageUpload', '|',
                    'undo', 'redo'],
    },
}

# --- Production xavfsizlik sozlamalari ------------------------------------
# HTTPS majburiy yo'naltirish FAQAT haqiqiy domenda, SSL sertifikat mavjud bo'lganda yoqiladi.
# .env faylida DJANGO_USE_HTTPS=True qo'ysangiz (production serverda) ishga tushadi.
# Lokal (runserver, http://127.0.0.1) test paytida bu False bo'lib qoladi.
USE_HTTPS = os.environ.get("DJANGO_USE_HTTPS", "False") == "True"

if USE_HTTPS:
    SECURE_SSL_REDIRECT = True            # barcha trafikni HTTPS'ga yo'naltiradi
    SESSION_COOKIE_SECURE = True          # cookie faqat HTTPS orqali yuboriladi
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000        # brauzerga doim HTTPS ishlatishni buyuradi
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

if not DEBUG:
    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Admin panel manzilini standart /admin/ dan boshqa nomga o'zgartirish tavsiya etiladi
# (config/urls.py faylida ADMIN_URL o'zgaruvchisi orqali sozlanadi).
ADMIN_URL = os.environ.get("DJANGO_ADMIN_URL", "admin/")