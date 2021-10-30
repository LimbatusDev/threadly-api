from .base import *

ALLOWED_HOSTS = []
DEBUG = False

# twitter secrets
TWITTER_API_KEY = get_env_variable('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = get_env_variable('TWITTER_API_KEY_SECRET')

# qvapay secrets
QVAPAY_KEY = get_env_variable('QVAPAY_KEY')
QVAPAY_KEY_SECRET = get_env_variable('QVAPAY_KEY_SECRET')

