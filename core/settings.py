"""
Django settings for core project.
Author: Muhammad Noman
"""

from pathlib import Path
import os

'''# =============== BASE & SECURITY CONFIGURATION ==============='''
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-p=3-93xin6_y494m)=*xg!ros5qoq8*8(c3^h2==!82*l97z0i'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# =============== APPLICATION DEFINITION ===============
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-Party Apps
    'rest_framework',
    'crispy_forms',
    'crispy_tailwind',  # For tailwind with crispy
    'tailwind',
    'drf_yasg',
    'django_countries',
    'phonenumber_field',  # Uncomment this
    'cities_light',
    
    # Custom Apps
    'apps.dashboard',
    'apps.inventory_tracking',
    'apps.supplychain',
    'apps.main',
    'apps.order_fulfillment',
    'apps.products',
    'apps.shipment_monitoring',
    'apps.accounts',
    'apps.utils',
    'apps.cart',
]

# =============== TAILWIND CONFIGURATION ===============
TAILWIND_APP_NAME = 'theme'  # Create this app with: python manage.py tailwind init theme
INTERNAL_IPS = ['127.0.0.1']
NPM_BIN_PATH = r'C:\Program Files\nodejs\npm.cmd'  # Windows path, change for your OS

# =============== CRISPY FORMS ===============
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# =============== CITIES LIGHT CONFIG ===============
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['PK', 'US', 'GB', 'AE', 'SA']  # Focus on relevant countries
CITIES_LIGHT_INCLUDE_REGIONS = ['ALL']
CITIES_LIGHT_INCLUDE_CITIES = ['ALL']
CITIES_LIGHT_CITY_SOURCES = ["http://download.geonames.org/export/dump/cities5000.zip"]

# =============== DJANGO REST FRAMEWORK ===============
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# =============== CUSTOM USER MODEL ===============
AUTH_USER_MODEL = 'accounts.User'

# =============== MIDDLEWARE ===============
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============== URL & TEMPLATES ===============
ROOT_URLCONF = 'core.urls'

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
                'django.template.context_processors.media',  # Add this
                'apps.cart.context_processors.cart_total',  # Custom context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# =============== DATABASE ===============
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 60,
        },
    }
}

# =============== PASSWORD VALIDATION ===============
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# =============== INTERNATIONALIZATION ===============
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'  # Changed to Pakistan time
USE_I18N = True
USE_TZ = True

# =============== STATIC & MEDIA FILES ===============
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============== DEFAULT AUTO FIELD ===============
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============== AUTHENTICATION ===============
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# =============== EMAIL CONFIGURATION ===============
# Add for password reset and notifications
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
# For production use:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-password'

# =============== JAZZMIN ADMIN ===============
JAZZMIN_SETTINGS = {
    "site_title": "Footwear Admin",
    "site_header": "Footwear Dashboard",
    "welcome_sign": "Welcome to Footwear Management System",
    "site_brand": "Footwear",
    "copyright": "© 2025 Muhammad Noman",
    "site_logo": None,
    "login_logo": None,
    "site_icon": None,
    
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "users"},
        {"app": "products"},
        {"app": "order_fulfillment"},
        {"app": "inventory_tracking"},
        {"app": "shipment_monitoring"},
        {"app": "supplier_monitoring"},
    ],
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_models": [],
    "order_with_respect_to": [
        "users",
        "products",
        "inventory_tracking",
        "order_fulfillment",
        "shipment_monitoring",
        "supplier_monitoring",
        "supplychain",
    ],
    
    "icons": {
        "auth": "fas fa-users-cog",
        "users.User": "fas fa-user",
        "users.Profile": "fas fa-id-card",
        "users.Address": "fas fa-map-marker-alt",
        "products": "fas fa-boxes",
        "products.Product": "fas fa-box",
        "products.Category": "fas fa-tags",
        "order_fulfillment": "fas fa-shopping-cart",
        "inventory_tracking": "fas fa-warehouse",
        "shipment_monitoring": "fas fa-shipping-fast",
        "supplier_monitoring": "fas fa-industry",
        "supplychain": "fas fa-project-diagram",
    },
    
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
    "related_modal_active": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark bg-dark",
    "sidebar": "sidebar-dark-primary",
    "brand_colour": "navbar-dark",
    "accent": "accent-info",
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "footer_fixed": False,
    "body_small_text": False,
    "sidebar_collapse": False,
    "actions_sticky_top": True,
}