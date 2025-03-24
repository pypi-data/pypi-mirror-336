from settings_common import *

SECRET_KEY = 'askhdbshfbkajdbuigd8qwgdiagsd897astf7aygsf6tvadn'

ADMINS = (
    ('Giovanni Mascellani', 'giovanni.mascellani@sns.it'),
)
ADMIN_EMAIL = 'geometriaglobale-owner@lists.math.unifi.it'
BULLETIN_EMAIL = 'geometriaglobale@lists.math.unifi.it'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gecogedi',
        'USER': 'gecogedi',
        'PASSWORD': 'kaewaeh0ahDei4ahChie',
        'HOST': 'localhost'
        }
    }

DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = False

SERVER_EMAIL = 'geometriaglobale-owner@lists.math.unifi.it'
SERVER_URL = 'http://gecogedi.dimai.unifi.it'
ALLOWED_HOSTS = ['gecogedi.dimai.unifi.it', 'calcio.math.unifi.it', '150.217.34.148']

HOSTNAME = 'gecogedi.dimai.unifi.it'
APACHE = True

GOOGLE_SITE_VERIFICATION = None

STATICFILES_DIRS = (
    os.path.join(BASE_ROOT, 'static-gecogedi'),
    os.path.join(BASE_ROOT, 'static'),
)

TEMPLATES[0]['DIRS'].insert(0, os.path.join(BASE_ROOT, 'templates-gecogedi'))

LIST_AUTHORS_BY_PAPERS = False
INSTANCE = 'gecogedi'
SITE_NAME = 'GeCo GeDi'
PREPRINT = ''

SHOW_SEMINAR_PLACE = True
SHOW_PARENTED_SEMINARS = False
