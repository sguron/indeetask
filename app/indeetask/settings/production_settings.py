"""Django STAGING settings for Instant-ACH project."""

import os

DB_HOST = os.environ.get('DB_HOST', 'mysqldb')
DB_PORT = os.environ.get('DB_PORT', '3306')

allowed_hosts = []

if "VIRTUAL_HOST" in os.environ:
    ALLOWED_HOSTS = [os.environ['VIRTUAL_HOST']]

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

