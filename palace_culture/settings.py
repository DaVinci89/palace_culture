"""
Django settings for palace_culture project.
"""
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонні додатки
    'django_htmx',
    'crispy_forms',
    #'crispy_forms_tailwind',

    # Наші додатки
    'pages.apps.PagesConfig',
    'events.apps.EventsConfig',
    'collectives.apps.CollectivesConfig',
    'news.apps.NewsConfig',
    'users.apps.UsersConfig',
    'about.apps.AboutConfig',
    'gallery.apps.GalleryConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'palace_culture.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'palace_culture.wsgi.application'

# База даних - PostgreSQL
DATABASES = {
    'default':
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite',
        dj_database_url.config(
            default="postgresql://neondb_owner:npg_i2IWrxPC8zeb@ep-patient-hill-aepzqkge-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
            conn_max_age=600,
            ssl_require=True,
        )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Налаштування Crispy Forms для Tailwind
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Додаткові налаштування безпеки (для продакшену)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'

# Налаштування email (для розробки)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'noreply@palace-culture.ua'

# Налаштування сесій
SESSION_COOKIE_AGE = 1209600  # 2 тижні
SESSION_SAVE_EVERY_REQUEST = True


# Для CSRF захисту
CSRF_TRUSTED_ORIGINS = [
    'https://euphemistic-ezequiel-repealable.ngrok-free.dev/',
]
# Налаштування для роботи через проксі (ngrok)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Налаштування SameSite для кук
SESSION_COOKIE_SAMESITE = 'None'  # або 'Lax'
CSRF_COOKIE_SAMESITE = 'None'     # або 'Lax'
# Якщо встановлено 'None', то також потрібно встановити:
SESSION_COOKIE_SAMESITE_FORCE_ALL = True  # Django 4.1+
CSRF_COOKIE_SAMESITE_FORCE_ALL = True     # Django 4.1+

# Налаштування аутентифікації
AUTH_USER_MODEL = 'users.CustomUser'