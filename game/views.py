from django.db.models.query import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from accounts.models import CustomUser
from .models import Game, Question, Result, Answer, GameInstance
from .serializers import (
    GamesSerializer,
    QuestionsSerializer,
    ResultsSerializer,
    AnswersSerializer,
    GameInstanceSerializer
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import GamesCreatorOnlyCanChange, QuestionsCreatorOnlyCanChange, AnswersCreatorOnlyCanChange, ResultsCreatorOnlyCanChange
from rest_framework.response import Response


class GamesViewSet(viewsets.ModelViewSet):
    serializer_class = GamesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, GamesCreatorOnlyCanChange]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context["creator"] = self.request.data["creator"]
        except Exception as e:
            pass
        return context

    def get_queryset(self):
        if self.request.query_params:
            try:
                if self.request.query_params["name"]:
                    game_name = self.request.query_params["name"]
                    queryset = Game.objects.filter(name=game_name)
            except Exception as e:
                pass
            try:
                if self.request.query_params["creator"]:
                    creator_name = self.request.query_params["creator"]
                    queryset = Game.objects.filter(creator=creator_name)
            except Exception as e:
                pass
            try:
                if self.request.query_params["category"]:
                    game_category = self.request.query_params["category"]
                    queryset = Game.objects.filter(category=game_category)
            except Exception as e:
                pass
            try:
                if self.request.query_params["filtered"]:
                    queryset = Game.objects.exclude(questions__isnull=True)
            except Exception as e:
                pass
        else:
            queryset = Game.objects.all()
        return queryset

class QuestionsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionsSerializer
    permission_classes = [QuestionsCreatorOnlyCanChange]

    def get_queryset(self):
        return Question.objects.filter(game=self.kwargs["game_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context["game_pk"] = self.kwargs["game_pk"]
        except Exception as e:
            pass
        return context


class ResultsViewSet(viewsets.ModelViewSet):
    serializer_class = ResultsSerializer
    permission_classes = [ResultsCreatorOnlyCanChange]

    def get_queryset(self):
        return Result.objects.filter(game=self.kwargs["game_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context["game_pk"] = self.kwargs["game_pk"]
        except Exception as e:
            pass
        try:
            context["player"] = self.request.data["player"]
        except Exception as e:
            pass
        return context


class AnswersViewSet(viewsets.ModelViewSet):
    serializer_class = AnswersSerializer
    permission_classes = [AnswersCreatorOnlyCanChange]

    def get_queryset(self):
        return Answer.objects.filter(question=self.kwargs["question_pk"])

'''
Multiplayer Addition
'''

class GameInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = GameInstanceSerializer
    queryset = GameInstance.objects.all()

class GameInstanceSlugViewSet(viewsets.ModelViewSet):
    
    def retrieve(self, request, slug=None, *args, **kwargs):
        queryset = GameInstance.objects.all()
        gameinstance = get_object_or_404(queryset, slug=slug)
        try:
            new_result = {}
            serializer = GameInstanceSerializer(gameinstance)
            new_result.update(serializer.data)
            new_result['creator'] = gameinstance.creator.username
            return Response(new_result)
        except:
            pass
        
        

        
