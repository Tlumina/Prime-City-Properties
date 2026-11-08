from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

import socket

# Check if PostgreSQL is listening on DB_HOST and DB_PORT
db_host = env('DB_HOST', default='localhost')
db_port = int(env('DB_PORT', default=5432))
use_sqlite = False

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.5)
    result = sock.connect_ex((db_host, db_port))
    sock.close()
    if result != 0:
        use_sqlite = True
except Exception:
    use_sqlite = True

if use_sqlite or env.bool('USE_SQLITE', default=False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Email to console in dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files in development
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
