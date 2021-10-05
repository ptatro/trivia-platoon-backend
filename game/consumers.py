from .models import GameInstance
from .serializers import GameInstanceSerializer

# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.mixins import ListModelMixin
# from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
# from djangochannelsrestframework.permissions import AllowAny
# from trivia.channelpermissions import CustomChannel

from channels.generic.websocket import AsyncWebsocketConsumer


# class GameInstanceConsumer(ListModelMixin, GenericAsyncAPIConsumer):
#     queryset = GameInstance.objects.all()
#     serializer_class = GameInstanceSerializer
#     permission_classes = (CustomChannel)

# class TestConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
#     queryset = GameInstance.objects.all()
#     serializer_class = GameInstanceSerializer
#     permission_classes = (CustomChannel)


class FooConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        user = self.scope["user"]
        await self.accept()
        print("Testing User", user)
        print("User properties", dir(user))
        print("User auth status", user.is_authenticated)