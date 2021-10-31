from django.db import models
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ffc4c1c607de49489dc5b071b326727e",
                                                           client_secret="4fd9dfe58f914768b24a034e1da88c2b"))


class playList(models.Model):
    url = models.URLField(max_length=255, blank=False, null=False)
    count = models.IntegerField(default=0)

    def info(self):
        track = sp.track(self.url)
        return track
    

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
