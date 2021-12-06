from decouple import config

from .base import *

ALLOWED_HOSTS = ["isaniro.com", 'www.isaniro.com', '127.0.0.1']

SECRET_KEY = config("SECRET_KEY", cast=str)
DEBUG= True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'isancjhv_blog',
        'USER': 'isancjhv_blog_user',
        'PASSWORD': config('DB_PASS'),
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        }
    }
}

STATIC_ROOT = '/home/isancjhv/public_html/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = "/home/isancjhv/public_html/media/"
# IMAGEFIT_ROOT = os.path.join(BASE_DIR, 'public')
SITE_ID = 1


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
