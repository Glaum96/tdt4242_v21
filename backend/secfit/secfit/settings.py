"""
Django settings for secfit project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from .djangoHeroku import settings

# Get the GROUPID variable to accept connections from the application server and NGINX
groupid = os.environ.get("GROUPID", "0")

# Email configuration
# The host must be running within NTNU's VPN (vpn.ntnu.no) to allow this config
# Usage: https://docs.djangoproject.com/en/3.1/topics/email/#obtaining-an-instance-of-an-email-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mx.ntnu.no"
EMAIL_USE_TLS = False
EMAIL_PORT = 25


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

SECRET_KEY = "aqw(!p=^c00jlo$24uv46$n%epw@#1nppviqh#p4l9af3&^32f"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
    "10." + groupid + ".0.6",
    "10." + groupid + ".0.4",
    "molde.idi.ntnu.no",
    "10.0.2.2",
    "secfit-1-backend.herokuapp.com"
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "workouts.apps.WorkoutsConfig",
    "users.apps.UsersConfig",
    "comments.apps.CommentsConfig",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "secfit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "secfit.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

is_prod = os.environ.get("IS_HEROKU", None)

if is_prod:
    settings(locals())

if 'DATABASE_URL' in os.environ:
    import dj_database_url
    print("\n\n\n\n\nHEI\n\n\n\n\n\n")
    DATABASES = {'default': dj_database_url.config()}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# CORS Policy
CORS_ORIGIN_ALLOW_ALL = (
    True
)

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "secfit", "staticfiles")
STATIC_URL = "/static/"

# MEDIA FILES
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    #"DEFAULT_AUTHENTICATION_CLASSES": (
    #    "rest_framework_simplejwt.authentication.JWTAuthentication",
    #),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ),
}

AUTH_USER_MODEL = "users.User"

DEBUG = True
