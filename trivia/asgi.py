"""
ASGI config for trivia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trivia.settings")
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from .channelmiddleware import JwtAuthMiddlewareStack
from game.consumers import FooConsumer, EchoConsumer, GameInstanceConsumer





application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JwtAuthMiddlewareStack(
        URLRouter([
            url(r"^user", FooConsumer.as_asgi()),
            url(r"^echo", EchoConsumer.as_asgi()),
            url(r"^gameinstance", GameInstanceConsumer.as_asgi())
        ])
    ),
 })

