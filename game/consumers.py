from django.db import connection
from .models import GameInstance, Result, Game
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import CustomUser
from django.forms.models import model_to_dict
from urllib.parse import parse_qs

"""
Example Test Consumer with Notes
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

    def websocket_disconnect(self, event):
        # Get the player ID and create an instance of user to put into player field
        playerID = parse_qs(self.scope["query_string"].decode("utf8"))["player"][0]
        player = CustomUser.objects.get(pk=playerID)
        # Get the slug from the ws URL path
        prefix, slug = self.scope["path"].strip('/').split('/')
        # Get the game instance and player count using the slug
        gameinstance = GameInstance.objects.get(slug=slug)
        gameinstance.player.remove(player)
        playercount = len(gameinstance.player.all())
        lobby = f"{playercount} of {gameinstance.maxplayers}"
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(slug, 
            {
                "type": "chat.message",
                "text": {
                    "maxplayers" : gameinstance.maxplayers, 
                    "status" : gameinstance.status,
                    "playercount" : playercount, 
                    "slug" : gameinstance.slug,
                    "game" : gameinstance.game.id,
                    "questiontimer" : gameinstance.questiontimer,
                    "lobby" : lobby
                    },
            })
        # self.send({
        #         "type": "websocket.close",
        #     })
        return


    #client first connects
    def websocket_connect(self, event):
        
        # Get the player ID and create an instance of user to put into player field
        playerID = parse_qs(self.scope["query_string"].decode("utf8"))["player"][0]
        newplayer = CustomUser.objects.get(pk=playerID)

        # Get the slug from the ws URL path
        prefix, slug = self.scope["path"].strip('/').split('/')
        # Get the game instance and player count using the slug
        gameinstance = GameInstance.objects.get(slug=slug)
        if (gameinstance.status == "lobby"):
            #print("we are in the lobby")
            gameinstance.player.add(newplayer)
            connectionstatus = "connected"
        else: 
            #print("we are not in the lobby - the game is full")
            connectionstatus = "game is full"
            self.send({
                "type": "websocket.accept",
            })
            self.send({
                "type": "websocket.send",
                "text": connectionstatus
            })
            return
        playercount = len(gameinstance.player.all())

        # If the playercount equals max players tell client to start else tell client to wait
        # Setting a variable to handle this message trigger within consumer and not model
        if (playercount == gameinstance.maxplayers):
            lobby = "full"
            gameinstance.status="full"
            gameinstance.save()
        else:
            lobby = f"{playercount} of {gameinstance.maxplayers}"

        channel_layer = get_channel_layer()
        async_to_sync(self.channel_layer.group_add)(slug, self.channel_name)

        async_to_sync(channel_layer.group_send)(slug, 
            {
                "type": "chat.message",
                "text": {
                    "maxplayers" : gameinstance.maxplayers, 
                    "status" : gameinstance.status,
                    "playercount" : playercount, 
                    "slug" : gameinstance.slug,
                    "game" : gameinstance.game.id,
                    "questiontimer" : gameinstance.questiontimer,
                    "lobby" : lobby
                    },
            })
        self.send({
                "type": "websocket.accept",
            })
        self.send({
                "type": "websocket.send",
                "text": connectionstatus
            })

    # Method to handle messages and send text to clients
    def chat_message(self, event):
        
        data = json.dumps(event["text"])
        self.send(
            {
                "type": "websocket.send",
                "text": data,
            }
        )

    #Server recieves message and replies
    def websocket_receive(self, event):

        # Get playerID, slug, player instance, game instance, score and create results
        playerID = parse_qs(self.scope["query_string"].decode("utf8"))["player"][0]
        player = CustomUser.objects.get(pk=playerID)
        prefix, slug = self.scope["path"].strip('/').split('/')
        messagebody = json.loads(event["text"])
        results_list = []
        gameinstance = GameInstance.objects.get(slug=slug)
        game = Game.objects.get(pk=gameinstance.game.id)

        # Handle Creator Start Message
        try:
            if messagebody["creator_start"]:
                message_trigger = "start"
                gameinstance.status = "in_progress"
                gameinstance.save()
        except Exception as e:
            pass
        try:
            if messagebody["score"]: 
                # Handle Results Submitted
                Result.objects.create(game=game, player=player, score=messagebody["score"], gameinstance=gameinstance)
                resultcount = len(gameinstance.results.all())

                # If the resultcount equals max players send all results back else return waiting on other players
                # Setting a variable to handle this message trigger within consumer and not model
                
                if (resultcount == gameinstance.maxplayers):
                    message_trigger = "complete"
                    gameinstance.status = "done"
                    gameinstance.save()
                    all_results = gameinstance.results.all()
                    for result in all_results:
                        result_dict = model_to_dict(result)
                        username = CustomUser.objects.get(pk=result_dict["player"])
                        result_dict["username"]=username.username
                        results_list.append(result_dict)

                else:
                    message_trigger = "waiting for other players"
        except Exception as e:
            pass

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(slug, 
            {
                "type": "chat.message",
                "text": {
                    "Group Message" : "This went to group",
                    "message_trigger" : message_trigger,
                    "all_results" : results_list
                    },
            })

        self.send({
            "type": "websocket.send",
            "text": "message received"
        })

'''
Game Instance Chat Consumer with Group Messages
'''

class ChatConsumer(SyncConsumer):

    def websocket_disconnect(self, event):
        # Get the player ID and create an instance of user to put into player field
        playerID = parse_qs(self.scope["query_string"].decode("utf8"))["player"][0]
        player = CustomUser.objects.get(pk=playerID)
        # Get the slug from the ws URL path
        prefix, slug = self.scope["path"].strip('/').split('/')
        # Get the game instance and player count using the slug
        gameinstance = GameInstance.objects.get(slug=slug)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(slug, 
            {
                "type": "chat.message",
                "text": {
                    "chat_message" : f'{player.username} has left chat', 
                    },
            })
        # self.send({
        #         "type": "websocket.close",
        #     })
        return


    #client first connects
    def websocket_connect(self, event):
        
        # Get the player ID and create an instance of user to put into player field
        playerID = parse_qs(self.scope["query_string"].decode("utf8"))["player"][0]
        newplayer = CustomUser.objects.get(pk=playerID)

        # Get the slug from the ws URL path
        prefix, slug = self.scope["path"].strip('/').split('/')
        # Get the game instance and player count using the slug
        gameinstance = GameInstance.objects.get(slug=slug)
        if (gameinstance.status == "lobby"):
            connectionstatus = "connected"
        else: 
            #print("we are not in the lobby - the game is full")
            connectionstatus = "game is full"
            self.send({
                "type": "websocket.accept",
            })
            self.send({
                "type": "websocket.send",
                "text": connectionstatus
            })
            return

        channel_layer = get_channel_layer()
        async_to_sync(self.channel_layer.group_add)(slug, self.channel_name)

        async_to_sync(channel_layer.group_send)(slug, 
            {
                "type": "chat.message",
                "text": {
                    "chat_message" : f'Welcome to chat {newplayer.username}',
                    },
            })
        self.send({
                "type": "websocket.accept",
            })
        self.send({
                "type": "websocket.send",
                "text": connectionstatus
            })

    # Method to handle messages and send text to clients
    def chat_message(self, event):
        
        data = json.dumps(event["text"])
        self.send(
            {
                "type": "websocket.send",
                "text": data,
            }
        )

    #Server recieves message and replies
    def websocket_receive(self, event):

        # Get playerID, slug, player instance, game instance, score and create results
        playerID = parse_qs(self.scope["query_string"].decode("utf8"))["player"][0]
        player = CustomUser.objects.get(pk=playerID)
        prefix, slug = self.scope["path"].strip('/').split('/')
        messagebody = json.loads(event["text"])
        # results_list = []
        gameinstance = GameInstance.objects.get(slug=slug)
        game = Game.objects.get(pk=gameinstance.game.id)

        print(messagebody["client_chat"])
        chat_message = messagebody["client_chat"]

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(slug, 
            {
                "type": "chat.message",
                "text": {
                    "chat_message" : chat_message,
                    "username" : player.username,
                    },
            })

        self.send({
            "type": "websocket.send",
            "text": "message received"
        })


"""
2nd Example Test Consumer for Auth
"""

class FooConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        user = self.scope["user"]
        await self.accept()
        print("Testing User", user)
        print("User auth status", user.is_authenticated)