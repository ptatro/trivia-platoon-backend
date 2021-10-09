"""
Django settings for trivia project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ
import os
from datetime import timedelta
import django_heroku

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Raises Django's ImproperlyConfigured
# exception if AWS_REGION not in os.environ
AWS_REGION = env("AWS_REGION")

# Raises Django's ImproperlyConfigured
# exception if AWS_STORAGE_BUCKET_NAME not in os.environ
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

# Raises Django's ImproperlyConfigured
# exception if AWS_ACCESS_KEY_ID not in os.environ
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")

# Raises Django's ImproperlyConfigured
# exception if AWS_SECRET_ACCESS_KEY not in os.environ
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_S3_CALLING_FORMAT = "boto.s3.connection.OrdinaryCallingFormat"
AWS_PRELOAD_METADATA = True

if AWS_STORAGE_BUCKET_NAME:
    STATIC_URL = "https://%s.s3.%s.amazonaws.com/static/" % (
        AWS_STORAGE_BUCKET_NAME,
        AWS_REGION,
    )
    MEDIA_URL = "https://%s.s3.%s.amazonaws.com/media/" % (
        AWS_STORAGE_BUCKET_NAME,
        AWS_REGION,
    )
    STATICFILES_STORAGE = "trivia.customstorages.StaticStorage"
    DEFAULT_FILE_STORAGE = "trivia.customstorages.MediaStorage"
    STATICFILES_LOCATION = "static"  # name of folder within bucket
    MEDIAFILES_LOCATION = "media"  # name of folder within bucket
else:
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"

MEDIA_URL = os.environ.get("MEDIA_URL", MEDIA_URL)
STATIC_URL = os.environ.get("STATIC_URL", STATIC_URL)


def get_static_memcache():
    from urllib.parse import urlparse

    if os.environ.get("REDIS_URL", ""):
        redis_url = urlparse(os.environ.get("REDIS_URL"))
        return {
            "BACKEND": "redis_cache.RedisCache",
            "TIMEOUT": None,
            "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
            "OPTIONS": {
                "PASSWORD": redis_url.password,
                "DB": 0,
            },
        }
    return {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": None,
        "OPTIONS": {"MAX_ENTRIES": 5000},
    }


CACHES = {
    # Replace the default cache with your existing one (if you have any)
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "collectfast": get_static_memcache(),
}
COLLECTFAST_CACHE = "collectfast"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ['bcp-trivia.herokuapp.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "game",
    "accounts",
    "rest_framework_swagger",
    "storages",
    "channels",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "trivia.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["./trivia/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "trivia.wsgi.application"
ASGI_APPLICATION = "trivia.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "trivia",
    }
}

# Custom user model
AUTH_USER_MODEL = "accounts.CustomUser"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Base url to serve media files
MEDIA_URL = "/media/"
# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
    'https://bcp-trivia-front.herokuapp.com',
]
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("JWT",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

"""
Turn this on for production
"""

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ['REDIS_URL'],],
        },
        # "ROUTING": "chat.routing.channel_routing",
    },
}

#6379'redis://localhost:{$PORT}'("127.0.0.1", 6379)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [os.environ['REDIS_URL']],
        "OPTIONS": "django-redis.client.DefaultClient"
    }
}
"""
Turn on for testing
"""

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }

django_heroku.settings(locals())
