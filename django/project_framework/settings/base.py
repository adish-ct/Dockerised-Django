"""
Django settings for Dockerized Django project.

Generated by 'django-admin startproject' using Django 3.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from django.contrib.messages import constants as message_constants
from .env import env

# Set project directory and base directory.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

APPLICATION_NAME = env.str("APPLICATION_NAME", default="Dockerized Django")

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production! False if not in os.environ because of casting above
DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# Application definitions
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

# Custom based django apps definition with urls.py base url.
CUSTOM_APPS = {
	'core': 'core',
}

# Appeding custom apps to Django installed apps.
INSTALLED_APPS += CUSTOM_APPS.keys()

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_framework.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(PROJECT_DIR, 'templates/')],
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

WSGI_APPLICATION = 'project_framework.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
	'default': env.db(),
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env.str('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

# Media files (images, videos, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django logging configuration with rotating file handler.
# https://docs.djangoproject.com/en/3.2/topics/logging/

ENABLE_LOGGING = env.bool('ENABLE_LOGGING', default=True)
if ENABLE_LOGGING:
	# Get logging directory from env file, or set default 'logs'.
	LOGGING_DIR = os.path.join(BASE_DIR, env.str('LOGGING_DIR', default='logs'))
	if not os.path.exists(LOGGING_DIR):
		os.makedirs(LOGGING_DIR)

	LOGGING = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'standard': {
				'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
				'datefmt': "%d/%b/%Y %H:%M:%S"
			},
		},
		'handlers': {
			'logfile': {
				'level': 'DEBUG',
				'class': 'logging.handlers.TimedRotatingFileHandler',
				'filename': os.path.join(LOGGING_DIR, 'django.log'),
				'when': 'D',  # this specifies the interval
				'interval': 1,  # defaults to 1, only necessary for other values
				'backupCount': 30,  # how many backup file to keep, 30 days
				'formatter': 'standard',
			},
			'console': {
				'level': 'INFO',
				'class': 'logging.StreamHandler',
				'formatter': 'standard'
			},
		},
		'loggers': {
			'django': {
				'handlers': ['console'],
				'propagate': True,
				'level': 'WARN',
			},
			'django.db.backends': {
				'handlers': ['console'],
				'level': 'DEBUG',
				'propagate': False,
			},
			APPLICATION_NAME: {
				'handlers': ['console', 'logfile'],
				'level': 'DEBUG',
			},
		}
	}

	# Enable automatic logging of Django exceptions
	ENABLE_AUTO_LOGGING = env.bool('ENABLE_AUTO_LOGGING', default=True)
	if ENABLE_AUTO_LOGGING:
		MIDDLEWARE += ['project_framework.core.middleware.auto_logging_middleware.ExceptionAutoLoggingMiddleware']

# Enable Django Debug Toolbar
ENABLE_DEBUG_TOOLBAR = env.bool('ENABLE_DEBUG_TOOLBAR', default=False)
if ENABLE_DEBUG_TOOLBAR:
	INSTALLED_APPS += [
		'debug_toolbar',
	]
	MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
	DEBUG_TOOLBAR_CONFIG = {
		"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
	}

# This sets the mapping of message level to message tag,
# which is typically rendered as a CSS class in HTML. 
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}
