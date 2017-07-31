# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
import os

from django.db import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBROOT_DIR = os.path.join(BASE_DIR, "../../webroot/")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "../../webroot/")

SECRET_KEY = os.environ.get('PROJECT_SECRET_KEY')

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "isj.tm.edu.ro", "isj.tm.edu.ro:8080",
                 "www.isj.tm.edu.ro", "new.isj.tm.edu.ro", "192.168.1.248",
                 "217.73.174.42", "217.73.174.42:8080",
                 "isj.website", "www.isj.website", "46.101.150.229"]

INSTALLED_APPS = [
    # admin theme
    'material',
    # 'material.frontend',
    'material.admin',

    # standard packages
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django packages
    # 'django_nose',
    'django_jenkins',
    'captcha',
    'widget_tweaks',
    'django_cleanup',
    'tinymce',
    'django_extensions',
    'django_google_maps',
    'haystack',
    'phonenumber_field',

    # usual apps
    'authentication',
    'homepages',
    'school',
    'subject',
    'post',
    'event',
    'utility',
    'news',
    'gallery',
    'contact',
    'page',
    'search',
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

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=authentication, contact, event, gallery, news, page, post'
    ',school, subject',
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
                'config.context_processors.template_context',
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
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend'
        '.ElasticsearchSearchEngine',
        'URL': os.environ.get('HAYSTACK_URL') + ":9200",
        'INDEX_NAME': 'haystack',
        'INCLUDE_SPELLING': True,
    },
}


HAYSTACK_SEARCH_RESULTS_PER_PAGE = 4

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.NumericPasswordValidator',
    },
]

models.options.DEFAULT_NAMES += ("index_text",)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(WEBROOT_DIR, 'static/')
STATICFILES_DIRS = (os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                 "static"),)

NOCAPTCHA = True
RECAPTCHA_USE_SSL = False

AUTH_USER_MODEL = 'authentication.ExtendedUser'

LOGIN_REDIRECT_URL = '/admin/'

TINYMCE_JS_URL = '/static/tinymce/tinymce.js'
