import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', 'kinpinarts.com,www.kinpinarts.com')
os.environ.setdefault('DB_HOST', 'localhost')
os.environ.setdefault('DB_PORT', '3306')
# Sensitive keys — set these via cPanel Environment Variables so they are not in git:
# DJANGO_SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, EMAIL_PASSWORD

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
