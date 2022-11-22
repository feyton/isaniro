from decouple import config

from .base import *

ALLOWED_HOSTS = ["isaniro.com", 'www.isaniro.com', '127.0.0.1']

SECRET_KEY = config("SECRET_KEY", cast=str)
DEBUG = True

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

SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
ADMINS = (('Robert', 'info@isaniro.com'),)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '198.54.114.236'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'books@isaniro.com'
EMAIL_HOST_PASSWORD = config('HOST_PASS', default="admin@2020")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
