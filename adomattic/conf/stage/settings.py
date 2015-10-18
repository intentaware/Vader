from base import *

SITE_ID = 1

DEBUG = False

ALLOWED_HOSTS = [
    '.intentaware.com',  # Allow domain and subdomains
    '.intentaware.com.',  # Also allow FQDN and subdomains
]

BASE_URL = "http://stage.intentaware.com"

INSTALLED_APPS += (
    'rest_framework',
    'raven.contrib.django.raven_compat',
    'django.contrib.staticfiles',
)

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://b1b9cb8df048483295724db97fadd76c:7f95b0b35c154327a0cd24d6638eb1d8@app.getsentry.com/45852',
}

STATIC_URL = 'http://stage.intentaware.com/static/'
MEDIA_URL = 'http://stage.intentaware.com/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'vader',
        'USER': 'django',
        'PASSWORD': 'DZn#kF^zdMcAsmytQEVKe7!w',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STRIPE_KEY = 'sk_test_s0cxlb2a5kArqUwfSGeig5CI'
