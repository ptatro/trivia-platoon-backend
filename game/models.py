from django.db import models
from accounts.models import CustomUser
import uuid
from django.db.models import F
from django.core.validators import MinValueValidator, MaxValueValidator



def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename


class Game(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to=get_file_path, default="imageNotAvailable.jpg")
    description = models.TextField()
    category = models.CharField(max_length=255)
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="games"
    )
    rating_count = models.IntegerField(default=-1)
    rating_total = models.IntegerField(default=0)

    class Meta:
        ordering = (-F("rating_total")/F("rating_count"),)


class Question(models.Model):
    questionText = models.TextField()
    type = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="questions")


class Result(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="results")
    player = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="results"
    )
    score = models.IntegerField(default=0)
    rating = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ("-score",)


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=255)
    correct = models.BooleanField()

class GameInstance(models.Model):
    
    maxplayers = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(10)])
    status = models.CharField(max_length=25, default="lobby")
    slug = models.SlugField(unique=True)
    player = models.ManyToManyField(CustomUser, related_name="gameinstances")
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="gamesinstances"
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="gameinstances")
    questiontimer = models.IntegerField(default=15)
    