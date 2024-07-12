# chat/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from authentication.models import *
from rest_framework.permissions import IsAuthenticated


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

class Message(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # Get data from request
        dic=request.data
        user_id = request.user.id
        message = dic.get('message')
        
        if not message:
                return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Construct the chat message dictionary
        message_obj = {
            "type": "chat_message",
            "message": message,
            "user_id": user_id
        }

        layer = get_channel_layer()
        chat_room_name = '1'

        async_to_sync(layer.group_send)(str(chat_room_name), message_obj)
        return Response({"message": "Message Sent Successfully"} , status=status.HTTP_200_OK)
    

def caption_dashboard(request):
    return render(request, "chat/caption_dashboard.html")


def user_dashboard(request, room_name):
    print('room_name',room_name)
    return render(request, "chat/user_dashboard.html", {"room_name": room_name})


class OrderRide(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        order_details = {
            'from': request.data['from'],
            'to': request.data['to'],
            'car_type': request.data['car_type'],
            'price': request.data['price'],
            'order_id': request.data['order_id'],
            'user_id': request.user.id,
        }

        layer = get_channel_layer()
        async_to_sync(layer.group_send)('online_captains', {
            'type': 'send_ride_order',
            'order_details': order_details
        })

        return Response({"message": "Order sent to captains"}, status=status.HTTP_200_OK)
    

class SendMessage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        message = request.data['message']
        user_id = request.user.id
        captain_id = request.data['captain_id']

        user = CustomUser.objects.get(id=user_id)
        captain = CustomUser.objects.get(id=captain_id)

        user_details = {
            'name': user.name,
            'phone': user.phone,
            'email': user.email,
            'role': user.role,
            'ride_category': user.ride_category,
        }

        captain_details = {
            'name': captain.name,
            'phone': captain.phone,
            'email': captain.email,
            'role': captain.role,
            'ride_category': captain.ride_category,
        }


        room_group_name = f'user_{user_id}_captain_{captain_id}'

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(room_group_name, {
            'type': 'message',
            'message': message,
            'user_details': user_details,
            'captain_details': captain_details,
        })

        return Response({"message": "Message sent to user and captain"}, status=status.HTTP_200_OK)
    

class SendCaptionCoordinates(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.data['user_id']
        captain_id = request.user.id
        coordinates = {
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude']
        }

        room_group_name = f'user_{user_id}_captain_{captain_id}_coordinates'

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(room_group_name, {
            'type': 'coordinates_message',
            'coordinates': coordinates
        })

        return Response({"message": "Coordinates sent to user"}, status=status.HTTP_200_OK)