"""
ASGI config for ecommerce_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from products.consumers import ProductSoldCountConsumer
from .routing import websocket_urlpatterns  # Import the websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
