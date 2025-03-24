from settings_common import *

ADMINS = (
    ('Giovanni Mascellani', 'giovanni.mascellani@sns.it'),
)
ADMIN_EMAIL = 'mascellani+admin@poisson.phc.unipi.it'
BULLETIN_EMAIL = 'mascellani+bulletin@poisson.phc.unipi.it'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #    'NAME': 'gecogedi',
    #    'USER': 'gecogedi',
    #    'PASSWORD': 'kaewaeh0ahDei4ahChie',
    #    'HOST': 'localhost'
    #    }
    }

DEBUG = True

SERVER_EMAIL = 'mascellani+server@poisson.phc.unipi.it'
SERVER_URL = 'http://localhost:8000'
ALLOWED_HOSTS = ['127.0.0.1']

HOSTNAME = 'localhost'
APACHE = False

GOOGLE_SITE_VERIFICATION = None

STATICFILES_DIRS = (
    os.path.join(BASE_ROOT, 'static-gecogedi'),
    os.path.join(BASE_ROOT, 'static'),
)

TEMPLATES[0]['DIRS'].insert(0, os.path.join(BASE_ROOT, 'templates-gecogedi'))

LIST_AUTHORS_BY_PAPERS = False
INSTANCE = 'gecogedi'
SITE_NAME = 'GeCo GeDi devel'
PREPRINT = ''

SHOW_SEMINAR_PLACE = True
SHOW_PARENTED_SEMINARS = True
