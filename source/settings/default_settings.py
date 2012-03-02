import os
PROJECT_DIR = lambda base : os.path.abspath(os.path.join(os.path.dirname(__file__), '../', base).replace('\\','/'))

gettext = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# South shouldn't migrate on tests (It's pointless)
SOUTH_TESTS_MIGRATE = False
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'nl'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

# Assures the proper locale directory is always loaded, even when using a differend settings file
LOCALE_PATHS = (
    PROJECT_DIR('locale'),
)

MEDIA_ROOT = PROJECT_DIR('media')
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_DIR('static')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '%sadmin/' % (STATIC_URL)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

#compressor
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sass --scss --cache-location /tmp/.sass-cache/ {infile} {outfile}'),
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wrHZvftLoigbaaYt3zNWAQRtgtQEDr9qNyjKqwAbZTTzsAEDAd'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    PROJECT_DIR('templates')
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'south',
    'debug_toolbar',

    'core.api',

    'modules.projects',
    'modules.profiles',
    'modules.memberships',

    'client',
)

INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

#E-mail
SERVER_EMAIL = 'info@getlogic.nl'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_SUBJECT_PREFIX = 'Local'

#Logging

LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
     'simple': {
            'format': '[%(levelname)s] [%(asctime)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
   },
   'handlers': {
       'mail_admins': {
           'level': 'ERROR',
           'class': 'django.utils.log.AdminEmailHandler'
       }
   },
   'loggers': {
       'django.request':{
           'handlers': ['mail_admins'],
           'level': 'ERROR',
           'propagate': True,
       },
   }
}


LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'simple',
}

API_TIMESTAMP_TIMEOUT = 60
