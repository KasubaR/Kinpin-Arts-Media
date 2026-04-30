"""Production settings — set DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS in the environment."""

import os

from .base import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
    if h.strip()
]
