from django.db import models
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ffc4c1c607de49489dc5b071b326727e",
                                                           client_secret="4fd9dfe58f914768b24a034e1da88c2b"))


class songModel(models.Model):
    artist = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    song = models.CharField(max_length=255)
    uri = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.song + " by " + self.artist


class playList(models.Model):
    url = models.URLField(max_length=255, blank=False, null=False, unique=True)
    song_list = models.ManyToManyField(songModel, related_name="playlist")
    count = models.IntegerField(default=0)

    def get_info(self):
        playlist = sp.playlist(self.url)
        return playlist

    def create_track(self):
        playlist_uri = self.get_info()
        a = playlist_uri['tracks']['items']
        for i in a:
            if not songModel.objects.filter(song=i['track']['name']).exists():
                song = songModel.objects.create(artist=i['track']['artists'][0]['name'],
                                                image=i['track']['album']['images'][0]['url'],
                                                song=i['track']['name'],
                                                uri=i['track']['preview_url'])

    def add_track_song_list(self):
        playlist_uri = self.get_info()
        a = playlist_uri['tracks']['items']
        for i in a:
            song = songModel.objects.get(song=i['track']['name'])
            self.song_list.add(song)
        self.save()

    def __str__(self):
        return self.url


class roomInfo(models.Model):
    player = models.ManyToManyField(
        settings.AUTH_USER_MODEL, null=True, blank=True) #1
    url = models.ForeignKey(playList, on_delete=models.CASCADE)
    ready_player = models.IntegerField(default=0)
    max_player = models.IntegerField(default=8)
    max_song = models.IntegerField(default=10)
    player_inroom = models.IntegerField(default=0)
    is_playing = models.BooleanField(default=False)


class played(models.Model): #2 
    played = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    room = models.ForeignKey(roomInfo, on_delete=models.CASCADE)
    max_score = models.IntegerField(default=10)
