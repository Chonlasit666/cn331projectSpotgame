# Generated by Django 3.2.8 on 2021-11-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotifymusicgame', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roominfo',
            name='guess_time',
        ),
        migrations.AddField(
            model_name='roominfo',
            name='player_inroom',
            field=models.IntegerField(default=0),
        ),
    ]