import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.espera.routing import websocket_urlpatterns  # Importa tus WebSockets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'velzon.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),  # WebSockets
})
