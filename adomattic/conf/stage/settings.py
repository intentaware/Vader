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
    'django_extensions',
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
        'USER': 'vader',
        'PASSWORD': 'e9x2055KK013Qjbz0S8ex5QA',
        'HOST': 'istage.c3udwfzrnadp.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

STRIPE_KEY = 'sk_test_s0cxlb2a5kArqUwfSGeig5CI'

BROKER_URL = 'amqp://vader:multiscan@rabbit/vader'
CELERY_RESULT_BACKEND = 'amqp://vader:multiscan@rabbit/vader'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
