# -*- coding: utf-8 -*-

import os

CONTENTDIR = os.path.dirname(__file__)
PROJECTDIR = os.path.dirname(CONTENTDIR)

# Files
MEDIA_ROOT = os.path.join(PROJECTDIR, 'content/uploads/')
MEDIA_URL = '/uploads/'
STATIC_ROOT = os.path.join(PROJECTDIR, 'content/static/')
STATIC_URL = '/static/'

# Admin panel settings
ADMIN_LOGIN_URL = '/manage/auth/login/'

# Options for testing.customrunner.CustomRunner
TEST_EXCLUDE = (
    'django_openid_auth',
    'crispy_forms',
    'django',
    'south',
    'imagekit',
)
TEST_RUN_ALL = False
TEST_RUNNER = 'testing.customrunner.CustomRunner'

STATICFILES_DIRS = (
    os.path.join(CONTENTDIR, 'static/'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(CONTENTDIR, 'templates/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.short_language_code',
                'common.context_processors.google_settings',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                'django.core.context_processors.request',
            ],
        },
    },
]

DEFAULT_FILE_STORAGE = 'common.storage.ASCIIFileSystemStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'common.http.Http403Middleware',
)

ROOT_URLCONF = 'Instanssi.urls'

INSTALLED_APPS = (
    'Instanssi.base_layout',
    'Instanssi.arkisto',
    'Instanssi.main2012',
    'Instanssi.main2013',
    'Instanssi.main2014',
    'Instanssi.main2015',
    'Instanssi.main2016',
    'Instanssi.admin_base',
    'Instanssi.admin_arkisto',
    'Instanssi.admin_blog',
    'Instanssi.admin_upload',
    'Instanssi.admin_slides',
    'Instanssi.admin_events',
    'Instanssi.admin_kompomaatti',
    'Instanssi.admin_users',
    'Instanssi.admin_profile',
    'Instanssi.admin_programme',
    'Instanssi.admin_events_overview',
    'Instanssi.admin_utils',
    'Instanssi.admin_screenshow',
    'Instanssi.admin_store',
    'Instanssi.users',
    'Instanssi.kompomaatti',
    'Instanssi.ext_blog',
    'Instanssi.ext_programme',
    'Instanssi.screenshow',
    'Instanssi.dblog',
    'Instanssi.json_api',
    'Instanssi.store',
    'Instanssi.infodesk',
    'imagekit',
    'twitter_tag',
    'crispy_forms',
    'social.apps.django_app.default',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'formtools',
)

# Authentication backends, notice the openid backend here.
AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.battlenet.BattleNetOAuth2',
    'social.backends.steam.SteamOpenId',
    'django.contrib.auth.backends.ModelBackend',
)


def make_cache_conf(debug_mode):
    if debug_mode:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake'
            }
        }
    else:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/tmp/instanssi_cache',
            }
        }


def make_email_conf(debug_mode):
    if debug_mode:
        return 'django.core.mail.backends.console.EmailBackend'
    else:
        return 'django.core.mail.backends.smtp.EmailBackend'
