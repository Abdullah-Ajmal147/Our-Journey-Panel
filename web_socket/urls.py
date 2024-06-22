from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('room/<str:room_name>/', room, name='room'),
    path('send_message/', SendMessage.as_view(), name='send-message'),

    path('order/<str:room_name>/', order, name='order'),
    path('order_ride/', OrderRide.as_view(), name='order-ride'),
]

