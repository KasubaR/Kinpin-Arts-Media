"""Local development settings."""

from .base import *

SECRET_KEY = 'django-insecure-sk33es*zqzd$jgc@s1vwa86ue=vn!#%&2l&7ww8sthwkv#t1pl'

DEBUG = True

ALLOWED_HOSTS: list[str] = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CONTACT_EMAIL = 'info@kinpinarts.com'
