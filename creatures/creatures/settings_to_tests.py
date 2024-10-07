from .settings import *  # noqa f403

del DEBUG_TOOLBAR_CONFIG  # noqa f821
del CELERY_RESULT_BACKEND  # noqa f821

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CELERY_BROKER_URL = 'memory://'
