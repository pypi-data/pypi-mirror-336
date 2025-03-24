import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cvgmt.settings-gecogedi")

import site
site.addsitedir('/home/gecogedi/venv/lib/python2.7/site-packages')

import sys
reload(sys)
sys.path.append('/home/gecogedi/cvgmt')
sys.setdefaultencoding('utf-8')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

