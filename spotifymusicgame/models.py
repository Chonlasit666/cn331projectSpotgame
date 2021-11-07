import json
from typing import Counter
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
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
        username = text_data_json['username']
        action = text_data_json['action']
        print("recive")

        if action == "chat" :
            message = text_data_json['message']
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
        
        elif action == "ready":
            await self.ready_users()
            # Send status to room group
            await self.channel_layer.group_send(
                self.room_group_name,
            {
                    'type': 'ready',
                    'username': username,
                    'action' : action,
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        action = event['action']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'action': action,
        }))

    #--------------------------------------------------
    # Receive message from room group
    async def ready(self, event):
        username = event['username']
        action = event['action']
        
        #print("receive" + action)
        max_user = await self.max_users()
        ready_user = await self.play()
        print(ready_user)
        #print(ready_user)
        if max_user <= ready_user :
            print("test play")
            action = "play"

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'action': action,
        }))


        
    @database_sync_to_async
    def max_users(self):
        max_user = roomInfo.objects.get(id=1).max_player
        return max_user


    @database_sync_to_async
    def ready_users(self):
        room_id =  self.room_name = self.scope['url_route']['kwargs']['room_name']
        update = roomInfo.objects.get(id=room_id)
        update.ready_player = update.ready_player + 1
        update.save()

    @database_sync_to_async
    def play(self):
        room_id =  self.room_name = self.scope['url_route']['kwargs']['room_name']
        current_user = roomInfo.objects.get(id=room_id).ready_player
 
        return current_user