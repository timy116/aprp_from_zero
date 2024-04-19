from .base import *


ALLOWED_HOSTS = ['*']
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
}

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']


NOTEBOOK_ARGUMENTS = [
    '--ip',
    '0.0.0.0',
    '--allow-root',
    '--no-browser',
]

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}