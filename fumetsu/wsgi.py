
import os
#import math
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fumetsu.settings')

application = get_wsgi_application()

app = application
