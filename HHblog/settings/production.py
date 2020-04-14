from .common import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

DJANGO_SECRET_KEY='ui3c&c-jqwh3-*4-8ywb9ej96xdqvmx5w85+5hjwlkilueig7i'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECRET_KEY = DJANGO_SECRET_KEY
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': os.environ['DB_ROOT_PASSWD'],
        'HOST': os.environ['DB_HOST'],
        # 'PASSWORD': 12345678,
        # 'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
