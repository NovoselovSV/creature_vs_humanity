import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--((konnfyz4%k_6c7u5^-l%k-gma!(1*qlp8#@j$g#h+5(+1na'

DEBUG = False

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
    'djoser',
    'core.apps.CoreConfig',
    'area.apps.AreaConfig',
    'beast.apps.BeastConfig',
    'nest.apps.NestConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]


if DEBUG:
    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

ROOT_URLCONF = 'creatures.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'creatures.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

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
CELERY_RESULT_EXPIRES = 600

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

AUTH_USER_MODEL = 'core.User'

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MAX_USERS_NAMES_LENGTH = 150
MAX_EMAIL_LENGTH = 254
MAX_CREATURE_NAMES_LENGTH = 150
MAX_AREA_NAMES_LENGTH = 150
BIRTH_PROCESS_TO_APPEAR = 100
BIRTH_KEY = 'nest_{nest.id}_giving_birth'
BEAST_ACTION_KEY = 'beast_{beast.id}_act'
BIRTH_TIME = 120
BUFFER_MULTIPLY = 3
BEAST_ACTING_TIME = 60
EARNING_BIRTH_PROCESS = 10
EARNING_EXPERIENCE = 100
MIN_CREATURE_TO_NEW_NEST = 10
NEW_LEVEL_EXPERIENTS = 1000
LVL_UP_ABILITY_NAME_VALUE = {
    'attack': 10,
    'defense': 1,
    'health': 100
}
FIRST_NEST_NAME = 'Nest of creatures'
FIRST_AREA_NAME = 'Поляна'
FIRST_AREA_DESCRIPTION = 'Поляна среди леса'
ATTACK_PORT = os.getenv('HUMANS_PORT', '8000')
ATTACK_HOST = os.getenv('HUMANS_HOST', 'http://humans')
ATTACK_URL = f'{ATTACK_HOST}:{ATTACK_PORT}/'
GROUP_ATTACK_ENDPOINT = 'groups/{group_id}/_defense/'
HQ_ATTACK_ENDPOINT = 'hq/{hq_id}/_defense/'
BEAST_SALT = os.getenv('BEAST_SALT', 'I\'m the beast')
HUMANS_SALT = os.getenv('HUMANS_SALT', 'I\'m only human')
