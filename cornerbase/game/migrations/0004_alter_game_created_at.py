# Generated by Django 3.2 on 2022-04-17 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_rename_created_on_game_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
