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
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default=config("EMAIL_HOST_USER", default="webmaster@localhost"),
)


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
    'rest_framework_simplejwt.token_blacklist',


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
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'AUTH_HEADER_TYPES': ('Bearer',),

    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
# ================= SPECTACULAR SETTINGS =================
SPECTACULAR_SETTINGS = {
    # ================= BASIC INFO =================
    'TITLE': 'Supply Chain Management API',
    'DESCRIPTION': 'Professional eCommerce / Marketplace API (Shop, Product, Seller System)',
    'VERSION': '1.0.0',

    # ================= SCHEMA CONTROL =================
    'SERVE_INCLUDE_SCHEMA': False,

    # ================= SWAGGER UI =================
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'displayRequestDuration': True,
        'filter': True,
    },

    # ================= TAG ORGANIZATION =================
    'TAGS': [
        {'name': 'Auth', 'description': 'Authentication & OTP'},
        {'name': 'Users', 'description': 'User management & roles'},
        {'name': 'Shop', 'description': 'Seller shop management'},
        {'name': 'Products', 'description': 'Product & inventory system'},
        {'name': 'Orders', 'description': 'Order processing system'},
    ],

    # ================= ENUM CLEANUP =================
    "ENUM_NAME_OVERRIDES": {
        "apps.products.choices.shop_status_choices.ShopStatusChoices": "ShopStatusEnum",
        "apps.products.choices.product_status_choices.ProductStatus": "ProductStatusEnum",
        "apps.users.choices.role_choices.UserRoleChoices": "UserRoleEnum",
        "apps.users.choices.status_choices.UserStatusChoices": "UserStatusEnum",
    },


    # ================= SCHEMA QUALITY =================
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_SPLIT_RESPONSE': True,

    'SORT_OPERATIONS': True,
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