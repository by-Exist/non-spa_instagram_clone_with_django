"""
WSGI config for instagram project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 수정됨
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram.settings.prod')

application = get_wsgi_application()
