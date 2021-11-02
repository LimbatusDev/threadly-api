from dotenv import load_dotenv

from .base import *

# We load the env vars from a .env file
load_dotenv()

ALLOWED_HOSTS = ["api.threadly.xyz"]
DEBUG = False

SECRET_KEY = get_env_variable('SECRET_KEY')

# email configuration
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = get_env_variable('EMAIL_PORT')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'CONN_MAX_AGE': 500,
        'ATOMIC_REQUESTS': True,
    }
}

# twitter secrets
TWITTER_API_KEY = get_env_variable('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = get_env_variable('TWITTER_API_KEY_SECRET')

# qvapay secrets
QVAPAY_APP_ID = get_env_variable('QVAPAY_APP_ID')
QVAPAY_APP_SECRET = get_env_variable('QVAPAY_APP_SECRET')

# for secrets requests
SECRET_TOKEN = get_env_variable('SECRET_TOKEN')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# add middleware to debug in production only for superusers
MIDDLEWARE.append('apps.core.middleware.UserBasedExceptionMiddleware')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': [],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'threadly-api': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'filters': [],
            'propagate': True
        }
    }
}

# security config
SECURE_HSTS_SECONDS = 3600  # 1 hours. 31536000 seconds = 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_SSL_REDIRECT = True  # check this
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'origin'
SECURE_HSTS_PRELOAD = True  # Without this, your site cannot be submitted to the browser preload list.

# cookies
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hour only
