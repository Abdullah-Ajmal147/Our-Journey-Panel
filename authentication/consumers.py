import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.ride_group_name = f'ride_{self.ride_id}'

        await self.channel_layer.group_add(
            self.ride_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.ride_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        location = text_data_json['location']

        await self.channel_layer.group_send(
            self.ride_group_name,
            {
                'type': 'location_message',
                'location': location
            }
        )

    async def location_message(self, event):
        location = event['location']

        await self.send(text_data=json.dumps({
            'location': location
        }))
