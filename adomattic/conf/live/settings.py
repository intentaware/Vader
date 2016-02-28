from base import *

SITE_ID = 1

DEBUG = False

ALLOWED_HOSTS = [
    '.intentaware.com',  # Allow domain and subdomains
    '.intentaware.com.',  # Also allow FQDN and subdomains
    'ec2-52-11-62-128.us-west-2.compute.amazonaws.com', # Temporary
]

BASE_URL = "https://app.intentaware.com"

INSTALLED_APPS += (
    'django.contrib.staticfiles',
    'storages',
)

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://b1b9cb8df048483295724db97fadd76c:7f95b0b35c154327a0cd24d6638eb1d8@app.getsentry.com/45852',
}

AWS_STORAGE_BUCKET_NAME = 'admtc'
AWS_ACCESS_KEY_ID = 'AKIAI23OY6DM5YW6IWIA'
AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_STORAGE = 'apps.common.utils.storage.StaticStorage'
DEFAULT_FILE_STORAGE = 'apps.common.utils.storage.MediaStorage'

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

STATIC_URL = "//%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
MEDIA_URL = "//%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'vader',
        'USER': 'vader',
        'PASSWORD': 'axBPx97Xx2pNDnphPvf6kWwXmqNbP3SNjSKVs32D',
        'HOST': 'vader.c3udwfzrnadp.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

STRIPE_KEY = 'sk_live_ykBdrWZnCW4YddbDDxrwm0dm'

GRAPH_URL = 'http://neo4j:plotograph@172.31.16.136/db/data/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
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
            'filename': '/srv/ia-live/logs/error-django.log',
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
            'level': 'DEBUG', # Or maybe INFO or DEBUG
            'propagate': True
        },
        'cities': {
            'handlers': ['log_to_stdout'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}
