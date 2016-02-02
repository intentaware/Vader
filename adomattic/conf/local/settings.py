from base import *

SITE_ID = 1

BASE_URL = 'http://localhost:9050'

INSTALLED_APPS += (
    'rest_framework',
    'devserver',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES += (
    'devserver.middleware.DevServerMiddleware',
)

INTERNAL_IPS = (
    '0.0.0.0', '127.0.0.1'
)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'vader',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
DATABASES = {
  'default': {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': 'test',
    'USER': os.environ.get('PG_USER'),
    'PASSWORD': os.environ.get('PG_PASSWORD'),
    'HOST': '127.0.0.1',
  }
}

DEVSERVER_MODULES = (
    #'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    #'devserver.modules.ajax.AjaxDumpModule',
    #'devserver.modules.profile.MemoryUseModule',
    #'devserver.modules.cache.CacheSummaryModule',
    #'devserver.modules.profile.LineProfilerModule',
)

DEVSERVER_TRUNCATE_SQL = False

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

STRIPE_KEY = 'sk_test_s0cxlb2a5kArqUwfSGeig5CI'

# Celery
# To run
# celery -A adomattic worker -l info
# you might want to change BROKER_URL and RESULT BACKEND as per you machine settings.
BROKER_URL = 'amqp://yousuf:adomattic@localhost/adomattic'
CELERY_RESULT_BACKEND = 'amqp://yousuf:adomattic@localhost/adomattic'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
