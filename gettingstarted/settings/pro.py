from .base import *

DEBUG = False
ADMINS = (
    ('Antonio M', 'email@mydomain.com'),
)
ALLOWED_HOSTS = ['gettingstartedproject_nenu.com', 'www.gettingstartedproject_nenu.com', '127.0.0.1']

DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'PORT': '5434',
    }
}
