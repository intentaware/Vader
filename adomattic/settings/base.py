"""

                               ```````....`````
                          ```..-/+oosyddddso+/:..```
                        ``-/sdmNMMMMNNMMMMNNMMNNds/-``
                     ``./ymMMMMMMMMM.+.MMMNNMMMMMMMmy:``
                    ``/hNMMMMMMMMMM::++:::NNMMMMMMMMMNy-``
                   `.sNMMMMMMMMMMMMM::++::NNMMMMMMMMMMMmo.`
                  `.smmMMMMMMMMMMMMMNN``MNNMMMMMMMMMMNNNo.`
                 `.odsNMMMM intentaware NMNNMMMMMMMMMMdsmN+``
                ``:my-ooydNMMMMMMMMMMNNMMMNNMMMMNmmmmNd-sNm-``
                `.ym/ ```./shdmmNNMMMNNMMMNNMNho+/::::+./mMs.`
               ``-md. ``.:shmNNNNNNNNNNMMMNmdhhdmmmmy::-.yMm-``
               ``/Nh `-/oNMMMMMMMMMMNNNMMMNdmNMMMMMMMNdysdMN+``
              ```sMmshhoymdyso+++osyhdmmmNmmmhyyssssyyhhhdNMy.`
               ..yMMMmso+-.....-----..-::/:-...----..``.--+md.``
               ..dMMd/..``.-.````...--oddh+/:--.......`````:h/``
              ``-mNy.`` `--`   `.--:/..+hy//+++:`    `..` ``-o-`
              ``yNy.`` `.-`   `.+ss+.``/ys:.---.`      ..` ` -/.`
             ``/Ny``   `-.      ```````-o+.`````       `.`    .:`
            ``-mh.``   `.`  ```..--:+s::s:`-:-..````   ``      -.
           ``.hh.``        `-ooosyyo/:-:o:./yddho/:-`  ``      ``
           ``od:``       `.../+ooo+:/+osys/://+sssyo-``
          ``/d/``        `..`.``````.-yMMNs.``````..---`
         ``-do `               `.:-..:hmmmh:`` ```
        ``.ys``               `-:::-``--:+-.. `.--`               .-
        ``oy``               `...--.`:s:od:.-` `.`  ..`           .+.
       ``+y.``             `.-.```/s:od:od:+h:``   -:.`          ` +o``
      ``-y-``             `./- ..-hy/yd/sd:om/..``-:.`           ` :h-``
      ``s+ `               -s/`-//ssoyysyhsyhsso.-s+``            ` ds`.
      ``+: `               -s/.+ooossssssooo++//.-o/``           ```ds`.
        ``                  ` ``.-:///////////-`  `              `.oy.``
                                 ``-://////:--.`                `-/:.`
                                    ``.--.```                    ```


Oh! you found the pathway to the dark side of the source, my young aprentice.
Remember, The dark side of the source is a pathway to many abilities some
consider to be ..... unnatural.

The first holocron towards your journey towards being a master ... here ..

    "Without strife, your victory has no meaning.
     Without strife, you do not advance.
     Without strife, there is only stagnation."

Embrace the wisdom and your journey will be complete!


https://docs.djangoproject.com/en/1.8/topics/settings/
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
#from django.conf.directives import app
CONF_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.join(CONF_DIR, os.pardir)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$r^ufp^!he)i22(@yw#+%y&%-)t3cdvipxbz4#s)g^5gifitt-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

BASE_APPS = (
    'apps.common',
)

DEFAULT_APPS = (
    #'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.humanize',
)

THIRD_PARTY_APPS = (
    # import export
    'import_export',

    'widget_tweaks',
    'corsheaders',

    # mandrill
    'djrill',

    # haystack
    #'haystack',

    # django photologue
    'photologue',
    'sortedm2m',
)

PLUGIN_APPS = (
    'plugins.cities',
    'plugins.census',
)

ADOMATIC_APPS = (
    'apps.users',
    'apps.companies',

    'apps.campaigns',
    'apps.impressions',

    'apps.guages',

    'apps.metas',
    'apps.finances',

    'apps.warehouse',

    # for front end
    'apps.dashboard',
)

INSTALLED_APPS = BASE_APPS + DEFAULT_APPS + THIRD_PARTY_APPS + PLUGIN_APPS + ADOMATIC_APPS

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'apps.common.middleware.ImpressionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'adomattic.urls'

WSGI_APPLICATION = 'adomattic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Moved to local

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Static Url is to be set as per the machine
#STATIC_URL = '/static/'

# Media files (All the uploads)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Media Url is to be set as per the machine
#MEDIA_URL = '/media/'

# Authentication (and Registration-Redux)
AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/users/auth/login/'
LOGOUT_URL = ''
LOGIN_REDIRECT_URL = '/dashboard/'

ACCOUNT_ACTIVATION_DAYS = 30


# For Registration process to be called from WordPress
REGISTRATION_API_KEY = 'WP_nEhj6FkTJNiFfiS5moVeUE'

# CORS Headers https://github.com/ottoyiu/django-cors-headers

#CORS_ORIGIN_REGEX_WHITELIST = (
#    '^(http?://)?(\w+\.)?adomattic\.com$',
#    '^(http?://)?localhost:9000$'
#)

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'wp-api-key',
    'publisher-key',
    'access-control-allow-origin',
    'access-control-allow-credentials'
)

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Impression Engine
IMPRESSION_COOKIE_NAME = 'magneto'

# Madrill
MANDRILL_API_KEY = "US9U8XiepMg6nUVDaq5UeQ"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
ADOMATTIC_FROM = "IntentAware <noreply@intentaware.com>"

# Stripe
STRIPE_KEY = 'sk_live_ykBdrWZnCW4YddbDDxrwm0dm'

# GRAPPELLI SETTINGS
# GRAPPELLI_ADMIN_TITLE = 'IntentAware Administration Console'
ADMIN_SITE_HEADER = 'IntentAware Administration Console'

# MAX MIND GEO IP2 Database File Root
MAXMIND_DB_ROOT = os.path.join(CONF_DIR, 'ipdb')
MAXMIND_CITY_DB = MAXMIND_DB_ROOT + '/GeoLite2-City.mmdb'
MAXMIND_CLIENTID = '106847'
MAXMIND_SECRET = 'JfADx8je3tMo'

# Plugin Cities
CITIES_POSTAL_CODES = ['ALL']
CITIES_LOCALES = ['en']
CITIES_PLUGINS = [
    #'cities.plugin.postal_code_ca.Plugin',  # Canada postal codes need region codes remapped to match geonames
    'plugins.cities.plugin.reset_queries.Plugin',  # plugin that helps to reduce memory usage when importing large datasets (e.g. "allCountries.zip")
]

# Google Geocode API
# GOOGLE_GEOCODE_KEY = 'AIzaSyCAT8k8LnKNPPnQcsGzLWuO7OhAh5tgCFo'
GOOGLE_GEOCODE_KEY = 'AIzaSyA4oLWxCyVdujsAxiQluF-CE_4403UUTzM'

# CENSUS URL
US_CENSUS_DB = {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': 'us_census',
    'USER': 'census',
    'PASSWORD': 'RnEnrChWdJUq9g6VTvhPbHEt8mRzW9We',
    'HOST': 'icensus.c3udwfzrnadp.us-west-2.rds.amazonaws.com',
    'PORT': '5432',
}

# Mocking IP for simulating census data
CENSUS_MOCK_IP = '99.235.58.170'


try:
    from local import *
except ImportError:
    sys.exit('Unable to import environment specific settings, check if file local.py is properly placed')
