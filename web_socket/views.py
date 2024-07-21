# chat/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from authentication.models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Message
from django.db.models import Q


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

class TestMessage(APIView):
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
    


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        sender_id = request.user.id
        # sender_id = request.query_params.get('sender')
        receiver_id = request.query_params.get('receiver')
        
        if sender_id and receiver_id:
            messages = Message.objects.filter(
                Q(sender=sender_id, receiver=receiver_id) |
                Q(sender=receiver_id, receiver=sender_id)
            ).order_by('created_at')
            serializer = GetMessageSerializer(messages, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Senser and Receiver id requried"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        message_text = request.data['message']
        sender_id = request.user.id
        receiver_id = request.data['receiver']
        serializer = MessageSerializer(data={'message_text': message_text, 'sender': sender_id, 'receiver': receiver_id})
        if serializer.is_valid():
            serializer.save()

            sender = CustomUser.objects.get(id=sender_id)
            receiver = CustomUser.objects.get(id=receiver_id)

            sender_details = {
            'id' : sender.id,
            'name': sender.name,
            'phone': sender.phone,
            'email': sender.email,
            'role': sender.role,
            'ride_category': sender.ride_category,
            }

            receiver_details = {
                'id' : receiver.id,
                'name': receiver.name,
                'phone': receiver.phone,
                'email': receiver.email,
                'role': receiver.role,
                'ride_category': receiver.ride_category,
            }

            room_group_name = f'sender_{sender_id}_receiver_{receiver_id}'

            layer = get_channel_layer()
            async_to_sync(layer.group_send)(room_group_name, {
                'type': 'message',
                'message': serializer.data,
                'sender': sender_details,
                'receiver': receiver_details,
            })
        
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk, format=None):
    #     message = self.get_object(pk)
    #     serializer = MessageSerializer(message, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     message = self.get_object(pk)
    #     message.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)