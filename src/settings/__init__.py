##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of T-Mon.
#
# T-Mon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# T-Mon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with T-Mon. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

from os import path

# FOLDERS
BASE_DIR = path.dirname(path.abspath(path.join(__file__, "..", "..")))
MEDIA_ROOT = path.join(BASE_DIR, "src", "static")
MEDIA_URL = "/static"
ROOT_URLCONF = "rjdj.tmon.server.urls"

# ADMIN
DEFAULT_FROM_EMAIL = "info@rjdj.me"
ADMIN_MEDIA_PREFIX = "/admin-static/"

# INTERNATIONALIZATION
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-us'
USE_I18N = False

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    path.join(BASE_DIR, "src/templates")
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'rjdj.djangotornado',
    'rjdj.tmon.server',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.syndication',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.auth',
)

TEMPLATE_EXTENSION = ".html"

GEOIP_DB_LOCATION = path.join(BASE_DIR, 'parts', 'GeoLiteCity.dat')

WEB_SERVICE_DB_PREFIX = "webservice"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
            'CULL_FREQUENCY': 2
        }
    }
}

LOGIN_REDIRECT_URL = "/view/dashboard"
LOGIN_URL = "/login"

MAX_BATCH_ENTRIES = 20

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(module)s.py: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s [%(asctime)s]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console-verbose': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        "null": {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
        'debug': {
            'handlers':['console-verbose'],
            'propagate': True,
            'level':'DEBUG',
        }
    }
}
