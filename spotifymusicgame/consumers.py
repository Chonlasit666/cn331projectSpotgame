import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
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
        await self.player_joinroom()
        #print("connected")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.player_leaveroom()
        #print("disconnected....")

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['username']
        action = text_data_json['action']
        
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
            message = text_data_json['message']
            await self.ready_users()
            # Send status to room group
            await self.channel_layer.group_send(
                self.room_group_name,
            {
                    'type': 'ready',
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
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'action': action,
        }))
        #await self.close()
        
    #--------------------------------------------------
    # Receive status from room group
    async def ready(self, event):
        message = "has ready!"
        username = event['username']
        action = event['action']
    
        play = await self.play()

        if play :
            action = "play"

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'action': action,
        }))

    @database_sync_to_async
    def ready_users(self):
        room_id =  self.room_name = self.scope['url_route']['kwargs']['room_name']
        update = roomInfo.objects.get(id=room_id)
        update.ready_player = update.ready_player + 1
        update.save()

    @database_sync_to_async
    def play(self):
        room_id =  self.room_name = self.scope['url_route']['kwargs']['room_name']
        flag = False
        current_ready_user = roomInfo.objects.get(id=room_id).ready_player
        max_user = roomInfo.objects.get(id=room_id).max_player
        if current_ready_user >= max_user :
            flag = True
 
        return flag

    @database_sync_to_async
    def player_joinroom(self):
        room_id =  self.room_name = self.scope['url_route']['kwargs']['room_name']
        current = roomInfo.objects.get(id=room_id)
        current.player_inroom = current.player_inroom + 1
        current.save()
        print(f"player in room {room_id} {current.player_inroom}")
        

    @database_sync_to_async
    def player_leaveroom(self):
        room_id =  self.room_name = self.scope['url_route']['kwargs']['room_name']
        current = roomInfo.objects.get(id=room_id)
        current.player_inroom = current.player_inroom - 1
        current.save()
        print("Player Disconnect")
        print(f"player in room {room_id} {current.player_inroom}")

        if current.player_inroom == 0 :
            current.delete()
        
        