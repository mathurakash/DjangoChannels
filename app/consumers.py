# Topic - Chat App with static Group name
from django.contrib.auth.models import User
from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer

from asgiref.sync import async_to_sync
import json
from.models import Chat,Group, User_Profile
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print('websocket connected....',event)
        print("Channel layer...",self.channel_layer)
        print("Channel Name...",self.channel_name)
        # async_to_sync(self.channel_layer.group_add)('programers',self.channel_name)

        print(self.scope['url_route']['kwargs']['group_name'])
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)
        self.send(
            {
                'type':'websocket.accept'
            }
        )

    def websocket_receive(self,event):
        print('message received from client....',event['text'])
        
        data=json.loads(event['text'])
    
        print("Data...........",data)
        
        print(self.scope['user'])
        group = Group.objects.get(name=self.group_name)
        
        if self.scope['user'].is_authenticated:
            chat=Chat(content=data['msg'],group=group)
            print(chat,'++++++++++++++++++++++++')
            chat.save()
            data['user']=self.scope['user'].username
            
            async_to_sync(self.channel_layer.group_send)(self.group_name,{
                'type':'chat.message',
                # 'message':event['text']
                'message':json.dumps(data)
            })
        else:
            self.send({
                'type':'websocket.send',
                'text':json.dumps({"msg":"Login Required","user":"Guest"})
            })


    def chat_message(self,event):
        print('Event......',event)
        print('actual data......',event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })


    def websocket_disconnect(self,event):
        print('websocket disconnected....',event)
        print("Channel layer...",self.channel_layer)
        print("Channel Name...",self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        raise StopConsumer()





class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print('websocket connected....',event)
        print("Channel layer...",self.channel_layer)
        print("Channel Name...",self.channel_name)
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.send(
            {
                'type':'websocket.accept'
            }
        )

    async def websocket_receive(self,event):
        print('message received from client....',event['text'])
        data=json.loads(event['text'])
        print("Data...........",data)
        print("Sender Data...........",data['sender'])
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        
        if self.scope['user'].is_authenticated:
            user=await database_sync_to_async(User.objects.get)(username=data['sender'])
            # print(user,type(user),'============================== User========================')
            sender = await database_sync_to_async(User_Profile.objects.get)(user=user)
            # print(sender,'============================== sender========================')
            # print(data['sender'],'==============================================')

            chat=Chat(content=data['msg'],group=group,sender=sender,timestamp=datetime.now())
            print(chat,'++++++++++++++++++++++++')
            await database_sync_to_async(chat.save)()
            data['user']=self.scope['user'].username
            await self.channel_layer.group_send(self.group_name,{
                'type':'chat.message',
                'message':json.dumps(data)
            })

            print('dump data.............',data)
        else:
            await self.send({
                'type':'websocket.send',
                'text':json.dumps({"msg":"Login Required","user":"guest"})
            })


    async def chat_message(self,event):
        print('Event......',event)
        print('actual data......',event['message'])
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })


    async def websocket_disconnect(self,event):
        print('websocket disconnected....',event)
        print("Channel layer...",self.channel_layer)
        print("Channel Name...",self.channel_name)
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        raise StopConsumer()


class CallConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # response to client, that we are connected.
        self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.my_name,
            self.channel_name
        )

    # Receive message from client WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json['type']

        if eventType == 'login':
            name = text_data_json['data']['name']

            # we will use this as room name as well
            self.my_name = name

            # Join room
            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )
        
        if eventType == 'call':
            name = text_data_json['data']['name']
            print(self.my_name, "is calling", name);
            # print(text_data_json)


            # to notify the callee we sent an event to the group name
            # and their's groun name is the name
            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'answer_call':
            # has received call from someone now notify the calling user
            # we can notify to the group with the caller name
            
            caller = text_data_json['data']['caller']
            # print(self.my_name, "is answering", caller, "calls.")

            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'ICEcandidate':

            user = text_data_json['data']['user']

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

    def call_received(self, event):

        # print(event)
        print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))


    def call_answered(self, event):

        # print(event)
        print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data']
        }))


    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({
            'type': 'ICEcandidate',
            'data': event['data']
        }))