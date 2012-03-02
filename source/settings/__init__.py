from django.core.exceptions import ImproperlyConfigured
try:
    from settings.local_settings import *
except ImportError:
    raise ImproperlyConfigured('Could not find the local_settings file')


if DATABASES['default']['NAME'] == '':
    raise ImproperlyConfigured("You didn't specify a database name")
