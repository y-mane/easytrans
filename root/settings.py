"""from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()"""
import environ
import os
import sys
from django.utils.translation import gettext_lazy as _
#from django.utils.translation import ugettexget_lazy as _


BASE_DIR = os.path.dirname(__file__)
PLATFORM_DIR = os.path.join(BASE_DIR, 'platforms')
# platform specific data to load: dev (developement) | prod (production)
PLATFORM = 'dev'
#PLATFORM = 'prod'
PLATFORM_TO_LOAD = os.path.join(PLATFORM_DIR, f"{PLATFORM}")
env = environ.Env()
env.read_env(os.path.join(PLATFORM_TO_LOAD, ".env"))


SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

#ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=list())
ALLOWED_HOSTS=['146.190.238.183','localhost','127.0.0.1']
ALLOWED_REMOTE_ORIGINS = env.list('ALLOWED_REMOTE_ORIGINS', default=list())
ALLOWED_REMOTE_HOSTS = []
BASE_APPS = [
    'start_form',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
"""DJANGO_LIVESYNC = {
    'PORT': 9001 # this is optional and is default set to 9001.
}"""

P_APPS = env.list('P_APPS', default=list())
INSTALLED_APPS = BASE_APPS + P_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'request.middleware.RequestMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
"""MIDDLEWARE_CLASSES = (
    'livereload.middleware.LiveReloadScript',
    'livesync.core.middleware.DjangoLiveSyncMiddleware',
)"""
ROOT_URLCONF = 'root.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'root.context_processors.root.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easytrans_3',
        'HOST':'localhost',
        'USERNAME':'keita',
        'PASSWORD':'keita08176279',
        'PORT': '5432',

    }
}

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':os.path.join( BASE_DIR ,'db.sqlite3'),
        'HOST':'localhost',
    },
    
}"""
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT='/home/keita/root/site/assets/'
#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': [
       'rest_framework.authentication.TokenAuthentication', 
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1", #6379
        "OPTIONS": {
            "PASSWORD": env('REDIS_PASS'),
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "cs_stickets"
    }
}
CACHE_TTL = 60 * 15

# Added Custom Settings
APP_TITLE = env('APP_TITLE')
LOGS_DIR = os.path.join(BASE_DIR, 'logs/')
DATE_INPUT_FORMATS = ['%d/%m/%Y']
LANGUAGE = (
    ('en', 'English'),
    ('fr', 'French'),
)
USE_THOUSAND_SEPARATOR = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
#  STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if 'test' in sys.argv:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'tmedia')

BARCODE_ROOT = os.path.join(MEDIA_ROOT, 'barcodes')
WEBSERVICES_CONFIG_FILE = os.path.join(BASE_DIR, 'webservices.cfg')
CONFIG_DIR = os.path.join(BASE_DIR, 'conf')
MESSAGES_FILE = 'messages.yaml'
#  FIXTURE_DIRS = os.path.join(BASE_DIR, 'fixtures')
#  FIXTURES_FILE = os.path.join(FIXTURE_DIRS, 'db.yaml')
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-spec', '--spec-color', '--nocapture', '--nologcapture']

# Email config
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('SERVER_EMAIL')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
TICKETS_ADMIN = env('TICKETS_ADMIN')
TICKETS_CONTACT = env('TICKETS_CONTACT')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
PAAS_MICROSERVICES_BASE_SERVER = env('PAAS_MICROSERVICES_BASE_SERVER')
PAAS_MICROSERVICES_SEND_EMAIL = '/emails/send/'
# Sessions
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 100
SESSION_SECURITY_WARN_AFTER = 840
SESSION_SECURITY_EXPIRE_AFTER = 900
SESSION_SECURITY_INSECURE = False
# List of url names middleware should ignore
#  SESSION_SECURITY_PASSIVE_URLS =
#  SESSION_SECURITY_PASSIVE_URLS_NAMES =

# Logging (Fr. Journalisation des évènements)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[ %(levelname)s ][ %(asctime)s ][ %(module)s ][ %(process)d ][ %(thread)d ] ==> %(message)s'
        },
        'simple': {
            'format': '[ %(levelname)s ][ %(asctime)s ][ %(module)s ] ==> %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'default.log'),
            'formatter': 'verbose',
        },
        'server': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'server.log'),
            'formatter': 'verbose',
        },
        'request': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'request.log'),
            'formatter': 'verbose',
        },
        'db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'db.log'),
            'formatter': 'simple',
        },
        'payment': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'payments.log'),
            'formatter': 'simple',
        },
        'api': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'api.log'),
            'formatter': 'simple',
        },
        'template': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'template.log'),
            'formatter': 'simple',
        },
        'access': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'access.log'),
            'formatter': 'simple',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(LOGS_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['server'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['template'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['db'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'default': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'accesslog': {
            'handlers': ['access'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'debug': {
            'handlers': ['debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'payment': {
            'handlers': ['payment'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['api'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'sentry': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Interface Configs
PAGE_NOT_FOUND = '404.html'
FORBIDDEN_ACCESS = '403.html'
INTERNAL_SERVER_ERROR = '500.html'
GOOGLE_RECAPTCHA_SECRET_KEY = env('GOOGLE_RECAPTCHA_SECRET_KEY')
GOOGLE_URL_CAPTCHA_CHECK = env('GOOGLE_URL_CAPTCHA_CHECK')
BASE_SERVER = env('BASE_SERVER')
CINETPAY_SITE_ID = env('CINETPAY_SITE_ID')
CINETPAY_APIKEY = env('CINETPAY_APIKEY')
CINETPAY_CHECK_STATUS_URL = env('CINETPAY_CHECK_STATUS_URL')
CINETPAY_GET_TXN_HISTORY_URL = env('CINETPAY_GET_TXN_HISTORY_URL')
