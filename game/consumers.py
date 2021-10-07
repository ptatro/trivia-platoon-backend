from .models import GameInstance
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

"""
Example Test Consumer
"""
class EchoConsumer(SyncConsumer):

    #client first connects
    def websocket_connect(self, event):
        
        self.send({
            "type": "websocket.accept",
        })

    #Server recieves message and replies
    def websocket_receive(self, event):
        # Access the body of the message from client with event["text"]
        # print(event["text"])
        
        # Example of turning json into a string to send to clien
        data = json.dumps({"keyname": "game is ready", "secondKey": "secret"})

        self.send({
            "type": "websocket.send",
            
            # this is the text returned and displayed to client
            # for json we'd need to turn it into a string
            # "text": data
            "text": event["text"]
        })

"""
Game Instance Consumer Working with Group Message on Connect
"""

class GameInstanceConsumer(SyncConsumer):

    #client first connects
    def websocket_connect(self, event):
        
        prefix, slug = self.scope["path"].strip('/').split('/')
        gameinstance = GameInstance.objects.get(slug=slug)

        channel_layer = get_channel_layer()
        async_to_sync(self.channel_layer.group_add)(slug, self.channel_name)

        async_to_sync(channel_layer.group_send)(slug, 
            {
                "type": "chat.message",
                "text": "Hello there!",
            })
        self.send({
            "type": "websocket.accept",
        })

    # Method to handle messages and send text to clients
    def chat_message(self, event):
        
        data = json.dumps({"Testing": event["text"]})
        self.send(
            {
                "type": "websocket.send",
                "text": data,
            }
        )

    #Server recieves message and replies
    def websocket_receive(self, event):
        # Access the body of the message from client with event["text"]
        # Example of turning json into a string to send to clien
        data = json.dumps({"keyname": "game is ready", "secondKey": "secret"})

        self.send({
            "type": "websocket.send",
            # this is the text returned and displayed to client
            # for json we'd need to turn it into a string
            # "text": data
            "text": event["text"]
        })

"""
2nd Example Test Consumer for Auth
"""

class FooConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        user = self.scope["user"]
        await self.accept()
        print("Testing User", user)
        # print("User properties", dir(user))
        print("User auth status", user.is_authenticated)