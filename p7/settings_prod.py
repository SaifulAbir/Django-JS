from p7.settings_dev import *

DEBUG=False
ALLOWED_HOSTS = ['*']
STATIC_ROOT = '/var/p7_static'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

