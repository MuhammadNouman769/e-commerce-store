"""
Django settings for core project.
Author: Muhammad Noman
"""

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


# ================= SECURITY =================
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=lambda v: [i.strip() for i in v.split(",")]
)


# ================= EMAIL =================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)

EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")


# ================= REDIS CACHE =================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# ================= APPLICATION DEFINITION =================
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'crispy_forms',
    'crispy_tailwind',
    'tailwind',
    'django_countries',
    'phonenumber_field',
    'cities_light',

    # API DOCS (NEW - SPECTACULAR)
    'drf_spectacular',

    # Custom apps
    'apps.dashboard',
    'apps.inventory_tracking',
    'apps.supplychain',
    'apps.main',
    'apps.order_fulfillment',
    'apps.products',
    'apps.shipment_monitoring',
    'apps.users',
    'apps.utils',
    'apps.cart',
]


# ================= TAILWIND =================
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']
NPM_BIN_PATH = r'C:\Program Files\nodejs\npm.cmd'


# ================= CRISPY FORMS =================
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


# ================= CITIES LIGHT =================
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['PK', 'US', 'GB', 'AE', 'SA']
CITIES_LIGHT_INCLUDE_REGIONS = ['ALL']
CITIES_LIGHT_INCLUDE_CITIES = ['ALL']


# ================= DJANGO REST FRAMEWORK =================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    #  SPECTACULAR SCHEMA
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}


# ================= SPECTACULAR SETTINGS =================
SPECTACULAR_SETTINGS = {
    'TITLE': 'Supply Chain Management API',
    'DESCRIPTION': 'API documentation for Supply Chain system',
    'VERSION': '1.0.0',
}


# ================= AUTH =================
AUTH_USER_MODEL = 'users.User'


# ================= MIDDLEWARE =================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ================= URLS =================
ROOT_URLCONF = 'core.urls'


# ================= TEMPLATES =================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


# ================= DATABASE =================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 60,
        },
    }
}


# ================= PASSWORD VALIDATION =================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ================= INTERNATIONALIZATION =================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True


# ================= STATIC & MEDIA =================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ================= DEFAULT AUTO FIELD =================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ================= AUTH REDIRECTS =================
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# ================= JAZZMIN ADMIN =================
JAZZMIN_SETTINGS = {
    "site_title": "BTR Mall Admin Dashboard",
    "site_header": "BTR Mall Dashboard",
    "welcome_sign": "Welcome to BTR Mall Management System",
    "site_brand": "BTR Mall Admin",
    "copyright": "© 2025 Muhammad Noman",

    "show_sidebar": True,
    "navigation_expanded": True,

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index"},
        {"app": "users"},
        {"app": "products"},
        {"app": "order_fulfillment"},
        {"app": "inventory_tracking"},
        {"app": "shipment_monitoring"},
        {"app": "supplychain"},
    ],
}


JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "accent": "accent-info",
}