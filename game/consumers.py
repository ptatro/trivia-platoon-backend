from .models import GameInstance, Result, Game
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import CustomUser
from django.forms.models import model_to_dict

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

    #client first connects
    def websocket_connect(self, event):
        
        # Can pass values in the headers but need to decode to string from bytes
        headers = self.scope["headers"]
        # print(headers[4][1].decode('UTF-8'))
        # Get the player ID and create an instance of user to put into player field
        playerID = headers[4][1].decode('UTF-8')
        newplayer = CustomUser.objects.get(pk=playerID)
        # print(newplayer)

        # Get the slug from the ws URL path
        prefix, slug = self.scope["path"].strip('/').split('/')
        # Get the game instance and player count using the slug
        gameinstance = GameInstance.objects.get(slug=slug)
        gameinstance.player.add(newplayer)
        playercount = len(gameinstance.player.all())

        # If the playercount equals max players tell client to start else tell client to wait
        # Setting a variable to handle this message trigger within consumer and not model
        if (playercount == gameinstance.maxplayers):
            message_trigger = "start"
        else:
            message_trigger = "wait"

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
                    "message_trigger" : message_trigger
                    },
            })
        self.send({
            "type": "websocket.accept",
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
        headers = self.scope["headers"]
        playerID = headers[4][1].decode('UTF-8')
        player = CustomUser.objects.get(pk=playerID)
        prefix, slug = self.scope["path"].strip('/').split('/')
        gameinstance = GameInstance.objects.get(slug=slug)
        game = Game.objects.get(pk=gameinstance.game.id)
        messagebody = json.loads(event["text"])
        Result.objects.create(game=game, player=player, score=messagebody["score"], gameinstance=gameinstance)
        resultcount = len(gameinstance.results.all())

        # If the resultcount equals max players send all results back else return waiting on other players
        # Setting a variable to handle this message trigger within consumer and not model
        results_list = []
        if (resultcount == gameinstance.maxplayers):
            message_trigger = "complete"
            all_results = gameinstance.results.all()
            for result in all_results:
                results_list.append(model_to_dict(result))
        else:
            message_trigger = "waiting for other players"

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(slug, 
            {
                "type": "chat.message",
                "text": {
                    "Group Message" : "Congrats the Game is Complete",
                    "message_trigger" : message_trigger,
                    "all_results" : results_list
                    },
            })

        self.send({
            "type": "websocket.send",
            "text": "results received"
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