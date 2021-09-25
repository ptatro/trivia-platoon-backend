from rest_framework_nested import routers
from .views import GamesViewSet, QuestionsViewSet, ResultsViewSet, AnswersViewSet
from django.urls import include
from django.conf.urls import url

game_router = routers.SimpleRouter()
game_router.register(r"games", GamesViewSet, basename="games")
result_router = routers.NestedSimpleRouter(game_router, r"games", lookup="game")
result_router.register(r"results", ResultsViewSet, basename="game-results")
question_router = routers.NestedSimpleRouter(game_router, r"games", lookup="game")
question_router.register(r"questions", QuestionsViewSet, basename="game-questions")
answer_router = routers.NestedSimpleRouter(question_router, r"questions", lookup="question")
answer_router.register(r"answers", AnswersViewSet, basename="question-answers")

urlpatterns = [
    url(r"^", include(game_router.urls)),
    url(r"^", include(result_router.urls)),
    url(r"^", include(question_router.urls)),
    url(r"^", include(answer_router.urls)),
]
