"""
Temporary helper settings used to dump data from the local SQLite database.
This module imports the main settings and overrides the database to SQLite.
"""
from ging_profile_v2.settings import *  # noqa: F401,F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
