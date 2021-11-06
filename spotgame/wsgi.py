"""
WSGI config for spotgame project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotgame.settings')


django_asgi_app = get_asgi_application()
