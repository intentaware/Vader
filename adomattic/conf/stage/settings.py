from base import *
import os

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
    'dsn':
    'https://b1b9cb8df048483295724db97fadd76c:7f95b0b35c154327a0cd24d6638eb1d8@app.getsentry.com/45852',
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
    },
    'us_census': US_CENSUS_DB
}

STRIPE_KEY = 'sk_test_s0cxlb2a5kArqUwfSGeig5CI'

BROKER_URL = 'amqp://vader:multiscan@rabbit/vader'
CELERY_RESULT_BACKEND = 'amqp://vader:multiscan@rabbit/vader'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format':
            '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[%(asctime)s]: %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'error-django.log'),
            'formatter': 'verbose',
        },
        'log_to_stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        # All the time, anywhere
        ' ': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True
        },
        # Again, default Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # All the apps
        'apps': {
            'handlers': ['logfile'],
            'level': 'DEBUG',  # Or maybe INFO or DEBUG
            'propagate': True
        },
        'cities': {
            'handlers': ['log_to_stdout'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}
