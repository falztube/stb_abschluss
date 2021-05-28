"""
Django settings for stb_abschluss project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from os import environ, path
from pathlib import Path
import django_heroku 
import dj_database_url
from decouple import config




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stb_abschluss.settings')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm&q)orr2a!12vu4#s2vmuiu)lgpsp&^)mz6g4q#g*lr&ar(g-h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django_plotly_dash.apps.DjangoPlotlyDashConfig', #hinzugefügt, für plotly
    'huftrends.apps.HuftrendsConfig', #hinzugefügt, eigene app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4', #hinzugefügt
    'channels', #für bootstrap
    'channels_redis', #für bootstrap
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'stb_abschluss.urls' 
                                

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'stb_abschluss.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {    
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },

    'meineDB': { 
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'meineDB', 
        'USER': 'postgres',
        'PASSWORD': 'super',
        'HOST': '127.0.0.1',
        'PORT': '5432'

    }
}


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

CRISPY_TEMPLATE_PACK = 'bootstrap4' # aus youtube tutorial

ASGI_APPLICATION = 'stb_abschluss.routing.application'  # aus youtube tutorial, damit bootstrap läuft

CHANNEL_LAYERS = {
    'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG' : {
                'hosts':['127.0.0.1', 8000], #auch für bootstrap
            }
        }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# aus youtube tutorial
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    
]
# aus youtube tutorial
PLOTLY_COMPONENTS = [
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dpd_components',
]
# aus youtube tutorial außer static_url    
STATICFILES_LOCATION = 'static'
STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = [BASE_DIR, 'stb_abschluss/static']

# für die Verwendung meherer Datenbanken, siehe db_routers.py
DATABASE_ROUTERS = ['routers.db_routers.Route_meineDB','routers.db_routers.Route_default']