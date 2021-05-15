"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&442jv50%6=(s8v#ge(l5&c=780zzf-v#4u-@onde$d95)s-25'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['easyquzy.herokuapp.com', '127.0.0.1']
# ALLOWED_HOSTS = ['192.168.10.143']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',
    'push_notifications',
    # 'django-celery-results',
    'channels',
    'user',
    'core',
    'room',
    
]

PUSH_NOTIFICATIONS_SETTINGS = {
        "FCM_API_KEY": "AAAA8x2B8oM:APA91bGs9iLgXdIUyol7RV_YFfSCyC3-pjywN7C6MzqOMenQHjxTKBWypsq8OYm_U_KYBkAzgBK-KoM3dktwReclaGkJnlLU2brSRu4h8oHipT70hSsUV3_crdKUGXHdqg0ajuOxwCrp",
        # "GCM_API_KEY": "[your api key]",
        # "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
        # "APNS_TOPIC": "com.example.push_test",
        # "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
        # "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
        # "WP_PRIVATE_KEY": "/path/to/your/private.pem",
        # "WP_CLAIMS": {'sub': "mailto: development@example.com"}
}

CELERY_BACKEND = 'redis://localhost:6379/3'
CELERY_BROKER_URL = 'redis://localhost:6379/4'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/5'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = True


# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
# CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Africa/Cairo'
CELERY_IMPORTS = (
    'room.tasks',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'
# Channels settings


# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],
#         },
#     },
# }


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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': os.environ.get('DB_HOST'),
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASS'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('Host'),
        'NAME': os.environ.get('Database'),
        'USER': os.environ.get('User'),
        'PASSWORD': os.environ.get('Password'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "app/static")]

# STATIC_URL = '/static/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_DIRS = [os.path.join(BASE_DIR, "app/media")]


# STATIC_ROOT = os.path.join(BASE_DIR, "vol/web/static")
# MEDIA_ROOT = os.path.join(BASE_DIR, "vol/web/media")
# STATIC_ROOT = 'vol/web/static'
# MEDIA_ROOT = 'vol/web/media'

# STATIC_ROOT = '/home/app/web/staticfiles'
# MEDIA_ROOT = '/home/app/web/mediafiles'

AUTH_USER_MODEL='core.User'

ASGI_APPLICATION = "app.routing.application"
# ASGI_APPLICATION = 'app.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('redis', 6379)],
#         },
#     },
# }

# CHANNELS_PRESENCE_MAX_AGE = 20 
