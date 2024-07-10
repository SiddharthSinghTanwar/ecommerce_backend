
from django.urls import path
from products.consumers import ProductSoldCountConsumer, EchoConsumer

websocket_urlpatterns = [
    path('ws/products/', ProductSoldCountConsumer.as_asgi()),
    path('ws/echo/', EchoConsumer.as_asgi()),
]