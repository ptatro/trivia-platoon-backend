from accounts.serializers import CustomUserSerializer
from rest_framework.serializers import ModelSerializer
from .models import Game, Result, Question, Answer
from accounts.models import CustomUser

class ResultsSerializer(ModelSerializer):
    class Meta:
        model = Result
        fields = ["id", "score", "rating", "player"]

    def create(self, validated_data):
        game = Game.objects.get(pk=self.context["game_pk"])
        result = Result.objects.create(game=game, **validated_data)
        try: 
            if result.rating: 
                game.rating_count += 1
                game.rating_total += result.rating
                game.save()
        except:
            pass
        return result


class AnswersSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "correct"]


class GamesSerializer(ModelSerializer):
    creator = CustomUserSerializer(read_only=True)
    class Meta:
        model = Game
        fields = ["id", "name", "image", "description", "category", "creator", 'rating_count', 'rating_total']

    def create(self, validated_data):
        creatorObj = CustomUser.objects.get(pk=self.context['creator'])
        game = Game.objects.create(creator=creatorObj, **validated_data)
        return game


class QuestionsSerializer(ModelSerializer):
    answers = AnswersSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "questionText", "type", "answers"]

    def create(self, validated_data):
        print(f"this is the validated data {validated_data}")
        answers_data = validated_data.pop('answers')
        game_pk = self.context["game_pk"]
        question = Question.objects.create(
            game=Game.objects.get(pk=game_pk), **validated_data
        )
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question
        
    def update(self, instance, validated_data):
        instance.questionText = validated_data.get('questionText', instance.questionText)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance