# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from authentication.models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope['url_route']['kwargs'])
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name =  self.room_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'data': text_data_json
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        data = event
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data': data
        }))


class RequestCaptainConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'online_captains'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     # Log the incoming data, useful for debugging
    #     print(f"Received data from captain: {text_data_json}")

    #     # Example of how to handle specific commands from captains
    #     command = text_data_json.get('command')
    #     if command == 'confirm_order':
    #         order_id = text_data_json.get('order_id')
    #         self.confirm_order(order_id)

    # def confirm_order(self, order_id):
    #     # Example response handling for order confirmation
    #     response = {'order_id': order_id, 'status': 'confirmed'}
    #     self.send(text_data=json.dumps(response))
        

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        if 'command' in data and data['command'] == 'confirm_order':
            print(data['captain_id'])
            self.confirm_order(data)

    def confirm_order(self, data):
        # Extract details from data
        order_id = data['order_id']
        user_id = data['user_id']
        user_name = data['user_name']
        phone = data['phone']
        country_code = data['country_code']
        email = data['email']
        role = data['role']
        from_address = data['from_address']
        from_latitude = data['from_latitude']
        from_longitude = data['from_longitude']
        to_address = data['to_address']
        to_latitude = data['to_latitude']
        to_longitude = data['to_longitude']
        care_type = data['care_type']
        fare = data['fare']

        captain_id = data['captain_id']

        captain_obj = CustomUser.objects.get(id=captain_id)
        print(captain_obj)
        

        # Send confirmation to the specific user
        layer = get_channel_layer()
        order_details = {
            "type": "user_message",
            "order_id": order_id,
            "user_id": user_id,
            "user_name": user_name,
            "phone": phone,
            "country_code": country_code,
            "email": email,
            "role": role,
            "from_address": from_address,
            "from_latitude": from_latitude,
            "from_longitude": from_longitude,
            "to_address": to_address,
            "to_latitude": to_latitude,
            "to_longitude": to_longitude,
            "care_type": care_type,
            "fare": fare,
            "message": "Order confirmation",
            "captain_id": captain_id,
            'captain_name':captain_obj.name,
            'captain_phone': captain_obj.phone,
            'captain_country_code': captain_obj.country_code,
            'captain_email': captain_obj.email,
            'captain_role': captain_obj.role,
            'captain_ride_category': captain_obj.ride_category,
        }

        user_id = user_id
        async_to_sync(layer.group_send)(str(user_id), order_details)

    def send_ride_order(self, event):
        order_details = event['order_details']
        self.send(text_data=json.dumps({
            'order_details': order_details
        }))



class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = self.user_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        order_details = text_data_json['order_details']

        # Send message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_message',
                'order_details': order_details
            }
        )

    def user_message(self, event):

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'order_details': event
        }))