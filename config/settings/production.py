import django_heroku

from .base import *

ALLOWED_HOSTS = []
DEBUG = False

# twitter secrets
TWITTER_API_KEY = get_env_variable('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = get_env_variable('TWITTER_API_KEY_SECRET')

# qvapay secrets
QVAPAY_APP_ID = get_env_variable('QVAPAY_APP_ID')
QVAPAY_APP_SECRET = get_env_variable('QVAPAY_APP_SECRET')

# for secrets requests
SECRET_TOKEN = get_env_variable('SECRET_TOKEN')

# Activate Django-Heroku.
django_heroku.settings(locals())
