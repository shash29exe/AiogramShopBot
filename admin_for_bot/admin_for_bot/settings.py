from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = r'C:\Users\Shash29\PycharmProjects\AiogramShopBot\media'
MEDIA_URL = '/media/'

SECRET_KEY = 'django-insecure-xr)i^ij2u#a7+&hx5t&(y!b5pa)0psl6w1l+3s=5+ttkqwk$fu'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_panel',
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'admin_for_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'admin_for_bot.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_ADDRESS'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {

    "search_model": ["admin_panel.User", "admin_panel.Category", "admin_panel.Product"],

    "topmenu_links": [
        {"name": "Главная", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],

    "icons": {
        "admin_panel.Users": "fas fa-user",
        "admin_panel.Categories": "fas fa-tag",
        "admin_panel.Products": "fas fa-cookie",

    },
    "show_sidebar": True,
        "navigation_expanded": True,
        "hide_apps": [],
        "order_with_respect_to": ["admin_panel", "auth"],
    }

JAZZMIN_UI_TWEAKS = {
    # darkly, cyborg, journal, lux, minty, solar, etc, flatly
    "theme": "darkly",

    # "navbar_small_text": False,
    # "footer_small_text": False,
    # "body_small_text": False,
    # "brand_color": "navbar-blue",
    # "accent": "accent-blue",
    "navbar": "navbar-black navbar-black",
    # "no_navbar_border": False,
    # "sidebar": "sidebar-light-blue",
    # "sidebar_nav_small_text": False,
}

