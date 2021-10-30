"""
This is the settings file that you use when you're working on the project locally.
Local development-specific include DEBUG mode, log level, and activation of developer tools like django-debug-toolsbar
"""

from dotenv import load_dotenv
from .base import *

# We load the env vars from a .env file
load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qov#ce&bl3z8@ymehv1byt^beru%el-0wjo%e#1q8#og6331ik'

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# twitter secrets
TWITTER_API_KEY = get_env_variable('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = get_env_variable('TWITTER_API_KEY_SECRET')

# qvapay secrets
QVAPAY_APP_ID = get_env_variable('QVAPAY_APP_ID')
QVAPAY_APP_SECRET = get_env_variable('QVAPAY_APP_SECRET')

# for secrets requests
SECRET_TOKEN = get_env_variable('SECRET_TOKEN')
