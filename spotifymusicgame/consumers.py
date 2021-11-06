import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import roomInfo
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        print(username)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        max_user = await self.max_users()
        print(max_user)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
    
    @database_sync_to_async
    def max_users(self):
        max_user = roomInfo.objects.get(id=1).max_player
        return max_user
    