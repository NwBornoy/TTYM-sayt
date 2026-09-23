"""
Qashqadaryo TTY sayti — Django sozlamalari.

Bu fayl UNIVERSAL production-ready ko'rinishda yozilgan — ya'ni PythonAnywhere,
VPS (Nginx/Gunicorn), yoki boshqa istalgan haqiqiy domenli serverda o'zgarishsiz ishlaydi.
Farq faqat .env faylidagi qiymatlarda bo'ladi, kod o'zgarmaydi.

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
    "jazzmin",
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
                "blog.context_processors.admin_notifications",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Ma'lumotlar bazasi ---------------------------------------------------
# Sinov uchun SQLite, production uchun DATABASE_URL orqali PostgreSQL tavsiya etiladi.
# Katta serverga o'tganda faqat .env faylida DATABASE_URL qiymatini qo'shsangiz kifoya,
# kod o'zgarmaydi.
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url  # pip install dj-database-url (agar postgres ishlatsangiz)
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,       # ulanishlarni 10 daqiqa "tirik" saqlaydi (tezlik uchun)
            conn_health_checks=True,
        )
    }
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
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "staticfiles"   # `collectstatic` shu yerga yig'adi

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# --- CKEditor 5 sozlamalari --------------------------------------------------
CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": ["heading", "|", "bold", "italic", "underline", "|",
                    "bulletedList", "numberedList", "|",
                    "link", "blockQuote", "imageUpload", "mediaEmbed", "|",
                    "undo", "redo"],
        "mediaEmbed": {
            "previewsInData": True,
        },
    },
}

# --- Email sozlamalari (xatolik xabarnomalari va parolni tiklash uchun) ---
# Katta serverda foydalanuvchilar parolni unutganda yoki serverda xato chiqqanda
# email yuborish uchun kerak bo'ladi. Hozircha .env bo'sh bo'lsa, konsolga chiqaradi.
EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("DJANGO_EMAIL_USE_TLS", "True") == "True"
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# Serverda 500-xato chiqsa, shu manzillarga avtomatik email keladi (DEBUG=False bo'lganda).
# .env faylida DJANGO_ADMIN_EMAIL=ismingiz@example.com qo'shsangiz ishga tushadi.
_admin_email = os.environ.get("DJANGO_ADMIN_EMAIL", "")
ADMINS = [("Admin", _admin_email)] if _admin_email else []
MANAGERS = ADMINS

# --- CSRF ishonchli manzillar ---------------------------------------------
# Django 4+ versiyalarida https orqali forma (login, admin va h.k.) yuborilganda
# domenning shu ro'yxatda bo'lishi shart, aks holda "CSRF verification failed" xatosi chiqadi.
# 127.0.0.1/localhost http orqali ishlagani uchun bu ro'yxatga kiritilmaydi.
# Kelajakda haqiqiy domen (masalan tibbiyordam.uz) qo'shilganda avtomatik shu yerga qo'shiladi —
# faqat .env'dagi DJANGO_ALLOWED_HOSTS'ga domenni yozish kifoya.
CSRF_TRUSTED_ORIGINS = [
    f"https://{h}" for h in ALLOWED_HOSTS if h not in ("127.0.0.1", "localhost")
]

# --- Production xavfsizlik sozlamalari ------------------------------------
# HTTPS majburiy yo'naltirish FAQAT haqiqiy domenda, SSL sertifikat mavjud bo'lganda yoqiladi.
# .env faylida DJANGO_USE_HTTPS=True qo'ysangiz (real domen/sertifikat bilan) ishga tushadi.
# Lokal (runserver, http://127.0.0.1) test paytida bu False bo'lib qoladi.
USE_HTTPS = os.environ.get("DJANGO_USE_HTTPS", "False") == "True"

if USE_HTTPS:
    # Ko'pchilik haqiqiy serverlarda (Nginx+Gunicorn, PythonAnywhere va boshqalar)
    # SSL sertifikat proxy serverda "tugaydi" — Django ilovasiga so'rov ICHKARIDA
    # http orqali yetib keladi, tashqaridan https ko'ringan taqdirda ham.
    # Shu sarlavha bo'lmasa, SECURE_SSL_REDIRECT doim qayta yo'naltirishga urinib,
    # "cheksiz redirect" (Too many redirects) xatosiga olib keladi.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True            # barcha trafikni HTTPS'ga yo'naltiradi
    SESSION_COOKIE_SECURE = True          # cookie faqat HTTPS orqali yuboriladi
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000        # brauzerga doim HTTPS ishlatishni buyuradi
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

if not DEBUG:
    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"   # YouTube embed (Error 153) uchun kerak

# Admin panel manzilini standart /admin/ dan boshqa nomga o'zgartirish tavsiya etiladi
# (config/urls.py faylida ADMIN_URL o'zgaruvchisi orqali sozlanadi).
ADMIN_URL = os.environ.get("DJANGO_ADMIN_URL", "admin/")

# --- Loglar (xatoliklarni kuzatish uchun) ---------------------------------
# Katta serverga o'tganda saytda nima xato ketayotganini fayldan ko'rish uchun juda foydali.
# Loglar BASE_DIR/logs/django.log fayliga yoziladi.
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} [{levelname}] {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR" if not DEBUG else "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "django.log",
            "maxBytes": 5 * 1024 * 1024,   # 5 MB dan oshsa, yangi faylga o'tadi
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "TTYM Admin",
    "site_header": "Qashqadaryo TTY",
    "site_brand": "TTYM Admin Panel",
    "welcome_sign": "Xush kelibsiz, Qashqadaryo TTYM boshqaruv paneliga",
    "copyright": "Qashqadaryo Tez Tibbiy Yordam Markazi",
    "search_model": ["blog.Post", "blog.Testimonial", "blog.Comment"],

    # Chap tomondagi menyu tartibi (ixtiyoriy — bo'limlarni guruhlash)
    "order_with_respect_to": [
        "auth",
        "blog.Testimonial",
        "blog.Comment",
        "blog.ErrorReport",
        "blog.SupportMessage",
        "blog.SupportTicket",
        "blog.Post",
        "blog.News",
        "blog.Branch",
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "blog.Post": "fas fa-newspaper",
        "blog.Testimonial": "fas fa-comment-medical",
        "blog.Comment": "fas fa-comments",
        "blog.News": "fas fa-bullhorn",
        "blog.Branch": "fas fa-hospital",
        "blog.Gallery": "fas fa-images",
        "blog.ContactInfo": "fas fa-phone",
        "blog.ErrorReport": "fas fa-exclamation-triangle",
        "blog.SupportTicket": "fas fa-life-ring",
        "blog.SupportMessage": "fas fa-envelope",
    },

    "show_ui_builder": True,   # Admin panelda o'zingiz rang/tema sozlashingiz mumkin bo'lgan tugma
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",   # boshqa temalar: cosmo, cyborg, darkly, lumen, solar, superhero va h.k.
}