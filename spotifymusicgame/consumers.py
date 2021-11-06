import json
from typing import Counter
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

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

        thisdict = {
        "brand": "Ford",
        }
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        action = text_data_json['action']


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'action' : action,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        action = event['action']
        
        #o_user = await self.users()
        #print(type(o_user))

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'action': action,
        }))