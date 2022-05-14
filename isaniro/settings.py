
import django_heroku
import dj_database_url
import os
from pathlib import Path
import cloudinary
import cloudinary.api
import cloudinary.uploader
from decouple import config

from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

MODE = config("MODE", cast=str, default="dev")
SECRET_KEY = config("SECRET_KEY", cast=str)
DEBUG = config("DEBUG", cast=bool, default=True)
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    "django_browser_reload",
    'blog',
    'services',
    'books',
    'user',
    'index',
    'django_social_share',
    # CK Editor
    'ckeditor',
    'ckeditor_uploader',
    # AllAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'hitcount',
    'rest_framework',
    'cloudinary',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware"

]

ROOT_URLCONF = 'isaniro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'isaniro.wsgi.application'

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



STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/"assets"
STATICFILES_DIRS = [BASE_DIR/"static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR/"media"

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },

}

# REGISTRATION-LOGIN URLS
LOGIN_URL = 'account_login'
LOGOUT_URL = 'account_logout'
LOGIN_REDIRECT_URL = 'home'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
AUTH_USER_MODEL = 'user.User'
# All Auth SETTINGS
SIGNUP_FORM_CLASS = 'user.forms.CreateUserForm'
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_FORM_CLASS = SIGNUP_FORM_CLASS
ACCOUNT_LOGIN_ON_EMAIL_COMFIRMATION = False
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Isaniro |'


def ACCOUNT_USER_DISPLAY(user):
    return user.get_full_name()


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# HITCOUNT_EXCLUDE_USER_GROUP = ( 'Editor', )
HITCOUNT_HITS_PER_IP_LIMIT = 0
HITCOUNT_KEEP_HIT_ACTIVE = {'days': 3}

cloudinary.config(cloud_name=config("cloud_name"), api_key=config(
    "api_key"), api_secret=config("api_secret"))

FLUTTER_SECRET = config("FLUTTER_SECRET")
BOOK_SIGNATURE = config("BOOK_SIGNATURE", default="dev")
SITE_ID = 1
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config('EMAIL_PASS')
if MODE == "production":
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    APPEND_SLASH = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    ADMINS = (('Fabrice', "tumbafabruce@gmail.com"),
              ("Spencer", "info@isaniro.com"))

    DATABASES = {
        'default': {

        }
    }
    DATABASES["default"] = dj_database_url.parse(config("DATABASE_URL"))


else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


CSRF_TRUSTED_ORIGINS = ["https://*.herokuapp.com",
                        'https://isaniro.com', 'https://isaniro.com', "http://*.herokuapp.com"]

django_heroku.settings(locals())
