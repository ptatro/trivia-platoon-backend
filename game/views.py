from .models import Game, Question, Result, Answer
from .serializers import GamesSerializer, QuestionsSerializer, ResultsSerializer, AnswersSerializer
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly

class GamesViewSet(viewsets.ModelViewSet):
    serializer_class = GamesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    #authentication_classes = ()

    def get_queryset(self):
        if self.request.query_params:
            try: 
                if self.request.query_params['name']:
                    game_name= self.request.query_params['name']
                    queryset = Game.objects.filter(name=game_name)
            except Exception as e:
                pass 
            try: 
                if self.request.query_params['creator']:
                    creator_name= self.request.query_params['creator']
                    queryset = Game.objects.filter(creator=creator_name)
            except Exception as e:
                pass 
        else:
            queryset = Game.objects.all()
        return queryset

class QuestionsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionsSerializer

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

    def get_queryset(self):
        return Result.objects.filter(game=self.kwargs["game_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context["game_pk"] = self.kwargs["game_pk"]
        except Exception as e:
            pass 
        return context

class AnswersViewSet(viewsets.ModelViewSet):
    serializer_class = AnswersSerializer

    def get_queryset(self):
        return Answer.objects.filter(question=self.kwargs["question_pk"])

