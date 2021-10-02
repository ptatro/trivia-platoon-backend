"""
ASGI config for trivia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from djangochannelsrestframework.consumers import view_as_consumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from game.views import GameInstanceConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trivia.settings")

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^websocket", view_as_consumer(GameInstanceConsumer)),
        ])
    ),
 })

