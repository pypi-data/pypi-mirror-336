import os
import sys
from dotenv import load_dotenv

path = os.path.dirname(os.path.dirname(__file__))

# load custom configuration
load_dotenv(dotenv_path=os.path.join(path,".env"))

sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'piprints.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
