# Generated by Django 3.2.7 on 2021-09-29 00:09

from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_result_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': (django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.F('rating_total'), '*', django.db.models.expressions.Value(-1)), '/', django.db.models.expressions.F('rating_count')),)},
        ),
    ]
