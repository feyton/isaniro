from decouple import config
from isaniro.settings import SITE_ID

from .base import *

ALLOWED_HOSTS = ["*"]

SECRET_KEY = 'django-insecure-5i&d(xd33wjb=vrqzfg3d32n3l_cpqm-!risebl^%1g8qpi4t8'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = 'home/isancjhv/public_html/static'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = "home/isancjhv/public_html/static"

SITE_ID = 1
