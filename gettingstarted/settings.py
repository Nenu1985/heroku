"""
Django settings for gettingstarted project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['nenuz.com', 'localhost', '127.0.0.1', 'c836bb8b.ngrok.io', 'nenu1985.herokuapp.com']
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.sites",
    # "django.contrib.sitemaps",
    "django.contrib.postgres",
    'sorl.thumbnail',
    'hello.apps.HelloConfig',
    'taggit',  # app for tagging functionality,
    'blog',
    'collage',
    'bootstrap3',
    'pizzashopapp',
    # 'djcelery',
    'celery_pb',
    'social_django',
    'account.apps.AccountConfig',
    'images.apps.ImagesConfig',




]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gettingstarted.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "gettingstarted.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": os.path.join(BASE_DIR, "db.sqlite3")
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'nenu',
        'PASSWORD': 'Nenu32590632',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'mele',
    #     'USER': 'postgres',
    #     'PASSWORD': 'Nenu32590632',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},

]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Minsk"

USE_I18N = True  #

USE_L10N = True

USE_TZ = True

LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout-django'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

GLOBAL_SETTINGS = {
    'FLICKR_PUBLIC': '1f9874c1a8ea5a85acfd419dd0c2c7e1',
    'FLICKR_SECRET': '67de04d2825fd397',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
UPLOAD_ASYNC = os.path.join(MEDIA_ROOT, 'upload_async')

django_heroku.settings(locals())

# -------  EMAIL SETTINGS  ------#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_PORT = 465  # 465 - SSL; 587 - TSL
EMAIL_HOST_USER = 'nenuzhny112018@gmail.com'
EMAIL_HOST_PASSWORD = 'nenu32590632'

# Celery settings

CELERY_BROKER_URL = 'redis://localhost'
#
# #: Only add pickle to this list if your broker is secured
# #: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False

#
#
#
# # Redis settings:
#
REDIS_BACKEND = {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0,
}
#
REDIS_BACKEND_URL = 'redis://{host}:{port}/{db}'.format(
    host=REDIS_BACKEND['HOST'],
    port=REDIS_BACKEND['PORT'],
    db=REDIS_BACKEND['DB'],
)

FILE_UPLOAD_HANDLERS = (
    "progressbarupload.uploadhandler.ProgressBarUploadHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # 'django': {
        #     'handlers': ['console'],
        #     'level': 'INFO',
        # },
    },
}

# google api key: AIzaSyBdvomEi7jeORG29PDt9crEq2Zvx42wHgY
# key=API_KEY
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'AIzaSyBdvomEi7jeORG29PDt9crEq2Zvx42wHgY'  # Google Consumer Key
# gogle client id: 931877487170-8lkvbsill09r7iat7qqu05tqa80p477m.apps.googleusercontent.com
# google secret client: Y_nU0dbLjQ2eVSpgyEvYtJi5

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '931877487170-8lkvbsill09r7iat7qqu05tqa80p477m.apps.googleusercontent.com' # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Y_nU0dbLjQ2eVSpgyEvYtJi5' # Google Consumer Secret
AUTHENTICATION_BACKENDS = {
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
    'social_core.backends.google.GoogleOAuth2',

}
