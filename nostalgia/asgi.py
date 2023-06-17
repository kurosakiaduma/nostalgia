"""
ASGI config for nostalgia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nostalgia.settings")

from channels.auth import AuthMiddlewareStack  
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack  
from django.core.asgi import get_asgi_application
from reactpy_django import REACTPY_WEBSOCKET_PATH 


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": SessionMiddlewareStack(
            AuthMiddlewareStack(URLRouter([REACTPY_WEBSOCKET_PATH]))
        ),
    }
)