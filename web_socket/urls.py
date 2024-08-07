from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('room/<str:room_name>/', room, name='room'),
    path('testmessage/', TestMessage.as_view(), name='message'),

    path('caption_dashboard/', caption_dashboard, name='caption_dashboard'),
    path('user_dashboard/<str:room_name>/', user_dashboard, name='user_dashboard'),
    path('order_ride/', OrderRide.as_view(), name='order-ride'),

    path('messages/', MessageView.as_view(), name='message-list-create'),
    path('send_coordinates/', SendCaptionCoordinates.as_view(), name='send_coordinates'),
]

