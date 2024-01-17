"""
Django settings for prosyndic project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = repertoire racine au meme niveau manage.py
BASE_DIR = Path(__file__).resolve().parent.parent
# Directory project au meme niveau de settings.py
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8f3yw@wajfef0^vqn^t9_6r!f_=c5&h^!nkxw$h@ktr5#j#rj3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'atlass.fr' ]

SITE_ID = 1
# email backend 
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # new


# Application definition

INSTALLED_APPS = [
    # local app 
    'copro.apps.CoproConfig',
    'accounts.apps.AccountsConfig',
    "polls.apps.PollsConfig",
    "cartcom.apps.CartcomConfig",
    "simulator.apps.SimulatorConfig",
    "drivedoc.apps.DrivedocConfig",
    
    # contribs
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework', # new
    # debug tools
    'debug_toolbar',
    # D- 3 rd party apps Django Rest Framework 
    'corsheaders', 
    # User Authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'markdownx', # <-- needed for adding markdown to forms
    
]

AUTH_USER_MODEL = "accounts.CustomUser" # new

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",  # new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    # debug 
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
# pour resoudre erreur No 'Access-Control-Allow-Origin' header is
CORS_ORIGIN_ALLOW_ALL = True
# Add here your frontend URL
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]

ROOT_URLCONF = 'prosyndic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
             os.path.join(BASE_DIR, 'copro', 'templates'),
             os.path.join(BASE_DIR, 'cartcom', 'templates', ),
             os.path.join(BASE_DIR, 'cartcom', 'templates', 'da'),
             os.path.join(BASE_DIR, 'cartcom', 'templates', 'cartcom'),
            ],
        
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

WSGI_APPLICATION = 'prosyndic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
	  'allauth.account.auth_backends.AuthenticationBackend',
    ]


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1 
# Sets the number of days within which an account should be activated. 

#ACCOUNT_EMAIL_REQUIRED = False
# set whether an email verification is necessary or not

#ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# Used to prevent brute force attacks.

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# User gets blocked from logging back in until a timeout.

ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400  # 1 day in seconds
# value set is in seconds from the last unsuccessful login attempt

ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

AUTH_USER_MODEL = "accounts.CustomUser"  # new


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static" )
# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
    os.path.join(BASE_DIR, 'media'),
    os.path.join(BASE_DIR, 'media', 'upload'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

REST_FRAMEWORK = {  # new
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        ## 'rest_framework.permissions.IsAdminUser'
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [  # new
        #"rest_framework.authentication.BasicAuthentication",  # enables simple command line authentication
        "rest_framework.authentication.SessionAuthentication",
        #"rest_framework.authentication.TokenAuthentication",  # new
    ],
}

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
)

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 
INTERNAL_IP = ['127.0.0.1']