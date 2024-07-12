# chat/routing.py
from django.urls import re_path

from web_socket import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/captain/$', consumers.RequestCaptainConsumer.as_asgi()),

    re_path(r'ws/user/(?P<user_id>\w+)/$', consumers.UserConsumer.as_asgi()),

    re_path(r'ws/one-to-one-chat/(?P<user_id>\w+)/(?P<captain_id>\w+)/$', consumers.UserCaptainConsumer.as_asgi()),
]