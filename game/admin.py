from django.contrib import admin
from .models import Game, Result, Answer, Question, GameInstance

admin.site.register(Game)
admin.site.register(Result)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(GameInstance)
