from decouple import config

from .base import *

ALLOWED_HOSTS = ["isaniro.com", 'www.isaniro.com', '127.0.0.1']

SECRET_KEY = config("SECRET_KEY", cast=str)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = '/home/isancjhv/public_html/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = "/home/isancjhv/public_html/media/"
IMAGEFIT_ROOT = os.path.join(BASE_DIR, 'public')
SITE_ID = 1


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
