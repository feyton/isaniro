from decouple import config
import django_heroku
from .base import *
import dj_database_url

ALLOWED_HOSTS = ["isaniro.herokuapp.com",
                 'www.isaniro.herokuapp.com', '127.0.0.1']

SECRET_KEY = config("SECRET_KEY", cast=str)
DEBUG = False

DATABASES = {
    'default': {

    }
}
DATABASES["default"] = dj_database_url.parse(config("DATABASE_URL"))

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/"assets"
STATICFILES_DIRS = [BASE_DIR/"static"]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR/"media"
SITE_ID = 1


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
ADMINS = (('Fabrice', 'tumbafabruce@gmail.com'),)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '198.54.114.236'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'books@isaniro.com'
EMAIL_HOST_PASSWORD = config('HOST_PASS')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

django_heroku.settings(locals())
