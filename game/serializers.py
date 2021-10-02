from accounts.serializers import CustomUserSerializer
from rest_framework.serializers import ModelSerializer
from .models import Game, Result, Question, Answer
from accounts.models import CustomUser


class ResultsSerializer(ModelSerializer):
    player = CustomUserSerializer(read_only=True)

    class Meta:
        model = Result
        fields = ["id", "score", "rating", "player"]

    def create(self, validated_data):
        game = Game.objects.get(pk=self.context["game_pk"])
        player = CustomUser.objects.get(pk=self.context["player"])
        result = Result.objects.create(game=game, player=player, **validated_data)
        try:
            if result.rating:
                if game.rating_count == -1:
                    game.rating_count += 2
                else:
                    game.rating_count += 1
                game.rating_total += result.rating
                game.save()
        except:
            pass
        return result

    def update(self, instance, validated_data):
        result_rating = instance.rating
        instance.score = validated_data.get("score", instance.score)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.save()
        game = instance.game
        try:
            if not result_rating:
                if game.rating_count == -1:
                    game.rating_count += 2
                else: 
                    game.rating_count += 1
                game.rating_total += instance.rating
                game.save()
    
        except:
            pass
        return instance


class AnswersSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "correct"]


class GamesSerializer(ModelSerializer):
    creator = CustomUserSerializer(read_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "image",
            "description",
            "category",
            "creator",
            "rating_count",
            "rating_total",
        ]

    def create(self, validated_data):
        creatorObj = CustomUser.objects.get(pk=self.context["creator"])
        game = Game.objects.create(creator=creatorObj, **validated_data)
        return game


class QuestionsSerializer(ModelSerializer):
    answers = AnswersSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "questionText", "type", "answers"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        game_pk = self.context["game_pk"]
        question = Question.objects.create(
            game=Game.objects.get(pk=game_pk), **validated_data
        )
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question

    def update(self, instance, validated_data):
        instance.questionText = validated_data.get(
            "questionText", instance.questionText
        )
        instance.type = validated_data.get("type", instance.type)
        instance.save()
        return instance
