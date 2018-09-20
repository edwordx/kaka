# -*- coding: utf-8 -*-

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'be5k77)sb2&c4$=bj05(u=yqcrjsg9=%2=mnst6r2&v0)ma5sck'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'kk',
    'admin_view_permission',
    'suit',
    'easy_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "raven.contrib.django.raven_compat",
    'captcha',
    'vuser',
    "shandianbao"
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kk.urls'

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

WSGI_APPLICATION = 'kk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
TIME_FORMAT = "H:i:s"
DATE_FORMAT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i:s"

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(pathname)s:%(lineno)d:: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'statistics': {
            'format': '%(asctime)s | %(levelname)s | %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s'
        },
        'record': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': "/var/log/kaka/debug.log",
            'level': 'ERROR',
        },
        'statistics_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'statistics',
            'filename': "/var/log/kaka/statistics.log",
            'level': 'DEBUG',
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['mail_admins', "file"],
            'level': 'ERROR',
            'propagate': True,
        },
        'statistics': {
            'handlers': ['statistics_handler'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}

if DEBUG:
    LOGGING = {}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_URL = '/vuser/login/'
LOGOUT_URL = '/vuser/logout/'
LOGIN_REDIRECT_URL = '/vuser/'

# for suit
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': u'营销平台',
    'HEADER_DATE_FORMAT': DATE_FORMAT,
    # 'HEADER_TIME_FORMAT': TIME_FORMAT,

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True,  # Default True

    # menu
    'SEARCH_URL': '',
    'MENU_OPEN_FIRST_CHILD': True,  # Default True
    'MENU': (
        # 'sites',
        {'app': 'auth', 'icon': 'icon-lock', 'models': ('user', 'group')},
        {'label': u'用户', 'app': 'vuser', 'icon': 'icon-user', 'models': ('UserProfile', )},
        {'label': u'微信用户', 'icon': 'icon-user', 'app': 'vuser', 'models': ('WXUser', )},
        {'label': u'闪电宝数据', 'icon': 'icon-heart', 'app': 'shandianbao', 'models': ('SDBTrade', 'SDBTerminal', 'SDBToken')},
        {'label': u'闪电宝用户信息', 'icon': 'icon-heart', 'app': 'shandianbao', 'models': ('SDBPos', )},
    ),

    # misc
    'LIST_PER_PAGE': 20
}
