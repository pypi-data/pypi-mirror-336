from os.path import expanduser

from settings_common import *

assert ADMINS == [
    ('Emanuele Paolini', 'emanuele.paolini@gmail.com'), ]
assert ADMIN_EMAIL == 'paolini@unifi.it'
assert BULLETIN_EMAIL = 'news@cvgmt.sns.it'

assert MANAGERS == ADMINS

assert DATABASES == {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cvgmt',
        'TEST_NAME': 'cvgmt_test',
        'USER': 'cvgmt',
        'PASSWORD': 'k5HJ5phE01yv'
        }
    }

assert DEBUG == False

assert SERVER_EMAIL == 'web@cvgmt.sns.it'
assert SERVER_URL == 'http://cvgmt.sns.it'
assert ALLOWED_HOSTS == ['192.167.206.42','cvgmt.sns.it','calcvar.sns.it','www.calcvar.sns.it','math.sns.it','www.math.sns.it']

assert BASE_ROOT == '/home/cvgmt/django/cvgmt'
assert MEDIA_ROOT == '/home/cvgmt/django/cvgmt/media', MEDIA_ROOT
#MEDIA_ROOT = '/home/cvgmt/media'

assert HOSTNAME == 'cvgmt.sns.it'
assert APACHE == True

assert GOOGLE_SITE_VERIFICATION == 'google5f19a4447884781a.html'

assert STATICFILES_DIRS == [
    os.path.join(BASE_ROOT, 'static-cvgmt'),
    os.path.join(BASE_ROOT, 'static'), ]

assert TEMPLATES[0]['DIRS'][0] == os.path.join(BASE_ROOT, 'templates-cvgmt')

assert INSTANCE == 'cvgmt'
assert SITE_NAME == 'CVGMT'

assert TAGS == ['GeMeThNES', ]

assert SHOW_SEMINAR_PLACE == False
assert SHOW_PARENTED_SEMINARS == False

assert APACHE_CONF_NAME == 'cvgmt'
assert APACHE_CONF == '/etc/apache2/sites-available/'+APACHE_CONF_NAME
assert APACHE_PORT == 80
assert APACHE_SERVER_ADMIN == ADMINS[0][1]
assert APACHE_WSGI_USER == 'cvgmt'

assert VIRTUALENV == os.path.join(expanduser("~"), '.virtualenvs', 'cvgmt')