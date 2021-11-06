# Generated by Django 3.2.8 on 2021-11-04 10:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spotifymusicgame', '0006_alter_playlist_song_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roominfo',
            name='player',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
