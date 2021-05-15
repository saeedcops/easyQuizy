
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from core.models import Room


@database_sync_to_async
def room_user_left(room_id,player_num):
    try:
        room = Room.objects.get(pk=room_id)
        if room.player1_profile==player_num and not room.player1_left:
            # print("user left 1")
            room.player1_score=-1
            room.player1_left=True
            room.save()
        elif room.player2_profile==player_num and not room.player2_left:
            # print("user left 2")
            room.player2_score=-1
            room.player2_left=True
            room.save()
        room.save()
        return room
    except Room.DoesNotExist:
        pass

@database_sync_to_async
def get_room(room_id):
    try:
        room = Room.objects.get(pk=room_id)
            
        return room
    except Room.DoesNotExist:
        return None


class RoomConsumer(AsyncWebsocketConsumer):

    player1=0
    player2=0
    is_random=False

    async def connect(self):

        if self.scope['user'].is_authenticated:
            # print("Accept")
            # Accept the connection
            await self.accept()
           
        else:
            # Reject the connection
            # print("is_anonymous")
            await self.close()
        
        self.sender=0
        self.qustion_num=0
        self.room_id = self.scope['url_route']['kwargs']['pk']
        self.group_name = "{}".format(self.room_id)
            # Join room group


        await self.channel_layer.group_add(
                        self.group_name,
                        self.channel_name
            )


    async def disconnect(self, close_code):

        player1score=0
        player2score=0
        room=await get_room(self.room_id)

        if room and not room.take_prize and not room.is_random:
    
            if self.scope['user'].pk == self.player1:
                # print("user 1")
                player1score=-1
                self.sender=self.player1

            elif self.scope['user'].pk == self.player2:
                # print("user 2")
                player2score=-1
                self.sender=self.player2
                

            await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'recieve_group_message',
                        'player1score':player1score,
                        'player2score':player2score,
                        'sender':self.sender,
                        'question':self.qustion_num,
                    }
                )

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        


    async def receive(self, text_data=None,bytes_data = None):

        text_data_json = json.loads(text_data)

        player1score = text_data_json['player1score']
        player2score = text_data_json['player2score']
        sender = text_data_json['sender']
        question= text_data_json['question']
    
        self.qustion_num=question
        self.sender=sender
        
    
        if self.player1==0:
            room =await get_room(self.room_id)
            self.player1=room.player1_profile
            
        if self.player2==0 :
            room =await get_room(self.room_id)
            self.player2=room.player2_profile
            
        

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'recieve_group_message',
                'player1score':player1score,
                'player2score':player2score,
                'sender':sender,
                'question':question,
            }
        )

        if player1score==-1 :
            
            await room_user_left(self.room_id,self.scope['user'].pk)
           
        elif player2score==-1:
            
            await room_user_left(self.room_id,self.scope['user'].pk)

        # call_command('random_player',self.room_id)
           


    async def recieve_group_message(self, event):

        player1score = event['player1score']
        player2score = event['player2score']
        sender = event['sender']
        question =event['question']

        if player1score==-1 and player2score==0:

            await self.send(
             text_data=json.dumps({
            'player1score':player1score,
            'player2score':player2score,
            'sender':sender,
            'question':question,
            }))
        elif player2score==-1 and player1score==0:

            await self.send(
             text_data=json.dumps({
            'player1score':player1score,
            'player2score':player2score,
            'sender':sender,
            'question':question,
            }))

        await self.send(
             text_data=json.dumps({
            'player1score':player1score,
            'player2score':player2score,
            'sender':sender,
            'question':question,
        }))
