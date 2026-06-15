"""
WSGI config for library_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from library_site.wsgi import application

app = application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_site.settings')

application = get_wsgi_application()
