from pathlib import Path
import socket
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')

print(f'SECRET_KEY :  {SECRET_KEY}')

SECRET_KEY = 'django-insecure-09r61b=!87jhzx3f7oxtqwgzgsvize%&*a$dq8+kz#h2p4%ii%'

print(f'after SECRET_KEY :  {SECRET_KEY}')

DEBUG = bool(int(os.environ.get('DEBUG', 0)))

DEBUG = os.getenv("DEBUG", "0") == "1"


ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(filter(None, os.environ.get('ALLOWED_HOSTS', '').split(',')))

print(f'✅ ALLOWED_HOSTS configured as: {ALLOWED_HOSTS}')

try:
    hostname_ip = socket.gethostbyname(socket.gethostname())
    ALLOWED_HOSTS.append(hostname_ip)
except Exception:
    pass

print(f'after ALLOWED_HOSTS configured as: {ALLOWED_HOSTS}')

CSRF_TRUSTED_ORIGINS = []
CSRF_TRUSTED_ORIGINS.extend(filter(None, os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')))
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

print(f'after ALLOWED CSRF_TRUSTED_ORIGINS_HOSTS configured as: {CSRF_TRUSTED_ORIGINS}')

# -----------------------------
# 🛠️ Hardcoded Project Settings
# -----------------------------

# Database Credentials
DB_NAME = 'dbname'
DB_USER = 'rootuser'
DB_PASS = 'changeme'

# Django Secret & Debug
SECRET_KEY = 'django-insecure-09r61b=!87jhzx3f7oxtqwgzgsvize%&+kz#h2p4%ii%'
DEBUG = False  # or True during local dev

# Runtime IDs
UID = 1001
GID = 1001

# Allowed Hosts
ALLOWED_HOSTS += [
    'neotechwave.com',
    'www.neotechwave.com',
    '127.0.0.1',
    'localhost',
    '172.167.156.234',
    'neotechwave.net',
    'www.neotechwave.net'
]

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS += [
    'https://neotechwave.net',
    'https://www.neotechwave.net',
    'https://*.127.0.0.1',
    'https://*.neotechwave.net'
]

# NGINX / TLS cert settings
# NGINX_SERVER_NAME = 'neotechwave.net www.neotechwave.net'
# CRT_DNS_ENV = 'neotechwave.net'

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_extensions',
    'main',
    'users',
    'questions',
    'analytics',
    'corsheaders',
    'whitenoise.runserver_nostatic',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHOD = 'username'
ACCOUNT_SIGNUP_FIELDS = ['username', 'password1', 'password2']
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_ON_SIGNUP = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]



ROOT_URLCONF = 'quizapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'quizapp.wsgi.application'

# DATABASE (SQLite for dev, replace with PostgreSQL in prod)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use this for PostgreSQL if needed:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASS'),
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': os.environ.get('DB_PORT', 5432),
#     }
# }

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC / MEDIA
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / "quizapp" / "static",
]
STATIC_ROOT = '/vol/web/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/vol/web/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ LOGGING (for gunicorn + AGIC debugging)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
