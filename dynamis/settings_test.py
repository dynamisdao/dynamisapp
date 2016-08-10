"""
This module exists purely so that environment configuration can be performed
for test runs.  Absolutely no special test configuration should be placed in
this file for any reason.
"""
import os


os.environ.setdefault('DATABASE_URL', 'sqlite://memory:')
os.environ.setdefault('DJANGO_SECRET_KEY', 'not-a-real-secret-key')
os.environ.setdefault(
    'DJANGO_EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend',
)
os.environ.setdefault('SITE_DOMAIN', 'test-domain')


from dynamis.settings import *  # NOQA
