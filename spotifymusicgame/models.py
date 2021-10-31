from django.db import models
from django.conf import settings

class playList(models.Model):
    url = models.URLField(max_length=255, blank=False, null=False)
    count = models.IntegerField(default=0)


class roomInfo(models.Model):
    player = models.ManyToManyField(
        settings.AUTH_USER_MODEL)
    url = models.ForeignKey(playList, on_delete=models.CASCADE)
    max_player = models.IntegerField(default=8)
    max_song = models.IntegerField(default=10)
    guess_time = models.IntegerField(default=15)


class played(models.Model):
    played = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    room = models.ForeignKey(roomInfo, on_delete=models.CASCADE)
    max_score = models.IntegerField(default=10)
