import os
from django.db import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/' # NU MAI MODIFICATI !! @ema
MEDIA_ROOT = os.path.join(BASE_DIR, "../media") # NU  MAI MODIFICATI !!!! @ema

SECRET_KEY = 'vl27lst+j0&n4ec$dh7qu^=i0f2@$#(dw-25#7$f##$w9s%8b5'

RECAPTCHA_PUBLIC_KEY = '6Le23xAUAAAAALeZVS6-CFTIKbhD-2XGYDWV3JUY'
RECAPTCHA_PRIVATE_KEY = '6Le23xAUAAAAADqwurHC-Cvm25zXqkvHuREZjiIo'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # admin theme
    'material',
    'material.frontend',
    'material.admin',
    
    # standard packages
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django packages
    'captcha',
    'widget_tweaks',
    'haystack',
    'django_cleanup',
    'tinymce',
    'django_extensions',
    
    # usual apps
    'authentication',
    'homepages',
    'school',
    'subject',
    'post',
    'headmaster',
    'inspector',
    'event',
    'view_permission',
    'news',
    'gallery'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'isj',
        'USER': 'isjuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Search engine config
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
    },
}
# Haystack index automatically
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

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

models.options.DEFAULT_NAMES += ("index_text", )

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

STATIC_URL = '/static/'
STATICFILES_DIRS = ( os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"), )

NOCAPTCHA = True
RECAPTCHA_USE_SSL = False

AUTH_USER_MODEL = 'authentication.ExtendedUser'

LOGIN_REDIRECT_URL = '/admin/'

TINYMCE_JS_URL = '/static/tinymce/tinymce.js'
