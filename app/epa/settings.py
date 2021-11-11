"""
Django settings for EPA project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import ast
import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'cdn_static_root')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('EPA_SECRET_KEY', 'v@p9^=@lc3#1u_xtx*^xhrv0l3li1(+8ik^k@g-_bzmexb0$7n')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(os.getenv('DEBUG', 'True'))

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    
    'users.apps.UsersConfig',
    'projects.apps.ProjectsConfig',
    'dashboard.apps.DashboardConfig',

    # 3rd Party
    'crispy_forms',
    'django_q',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'epa.urls'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'op_templates')],
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

WSGI_APPLICATION = 'epa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

USE_MYSQL_CONTAINER = ast.literal_eval(os.getenv('MYSQL_DB_CONTAINER', 'False'))
DATABASES = {
    # ELAND dockerized mysql container
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'open_plan-app-db',
        'USER': 'root',
        'PASSWORD': '4kFDg@G@*G,#)Fa',
        'HOST': 'db',
        'PORT': 3306,
    }
    if USE_MYSQL_CONTAINER else (
        # local with sqlite
        {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    )
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

LANGUAGES = [
    ('de', 'German'),
    ('en', 'English'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Other configs

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'project_search'
LOGOUT_REDIRECT_URL = 'home'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
MAILER_EMAIL_BACKEND = EMAIL_BACKEND

DEFAULT_FROM_EMAIL = 'noreply@elandh2020.eu'
EMAIL_HOST = os.getenv('EMAIL_HOST_IP', '127.0.0.1')
EMAIL_PORT = 25
EMAIL_USE_TLS = False

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

USE_PROXY=ast.literal_eval(os.getenv('USE_PROXY', 'True'))
PROXY_ADDRESS_LINK=os.getenv('PROXY_ADDRESS', 'http://icache.intracomtel.com:80')
PROXY_CONFIG = ({
    "http://": PROXY_ADDRESS_LINK,
    "https://": PROXY_ADDRESS_LINK,
}) if USE_PROXY else ({})

MVS_API_HOST=os.getenv('MVS_API_HOST', 'https://mvs-eland.rl-institut.de')
MVS_POST_URL = f"{MVS_API_HOST}/sendjson/"
MVS_GET_URL = f"{MVS_API_HOST}/check/"

# Allow iframes to show in page
X_FRAME_OPTIONS = 'SAMEORIGIN'

import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'dtlnm': {
            'format': '%(asctime)s - %(levelname)8s - %(name)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django_epa_info.log',
            'formatter': 'dtlnm'
        },
        'warnings_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'django_epa_warning.log',
            'formatter': 'dtlnm'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        '': {
            'handlers': ['info_file', 'warnings_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# DJANGO-Q CONFIGURATION
# source: https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    'name': 'django_q_orm',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'orm': 'default'
}
