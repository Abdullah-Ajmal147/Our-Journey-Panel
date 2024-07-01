import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import web_socket.routing

# Ensure DJANGO_SETTINGS_MODULE is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django application
django.setup()

# Import the ASGI application from your Django project's routing module
# from core.routing import application as django_application

# Combine Django ASGI application with WebSocket routing
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Django HTTP ASGI application
    "websocket": AuthMiddlewareStack(
        URLRouter(
            web_socket.routing.websocket_urlpatterns
        )
    ),
})
