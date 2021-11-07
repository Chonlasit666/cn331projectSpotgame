from django.test import TestCase
from .models import songModel, playList
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class songModelTest(TestCase):

    def setUp(self):
        song = songModel.objects.create(
            artist='sample', image='sample', song='sample', uri='sample')

    def test_return_songModel(self):
        song = songModel.objects.get(pk=1)
        self.assertEqual(song.song + ' by '+song.artist, str(song))


class playListTest(TestCase):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ffc4c1c607de49489dc5b071b326727e",
                                                               client_secret="4fd9dfe58f914768b24a034e1da88c2b"))
    url = 'spotify:playlist:4taxX9mVX4deBsqG6ffEbP'

    def setUp(self):
        url = self.url
        playlist = playList.objects.create(url=url)
        sp = self.sp
        playlist_uri = sp.playlist(url)
        a = playlist_uri['tracks']['items']
        for i in a:
            song = songModel.objects.create(artist=i['track']['artists'][0]['name'],
                                            image=i['track']['album']['images'][0]['url'],
                                            song=i['track']['name'],
                                            uri=i['track']['preview_url'])

    def test_return_playList(self):
        playlist = playList.objects.get(pk=1)
        self.assertEqual(playlist.url, str(playlist))
        
    def test_playList_get_info(self):
        sp = self.sp
        playlist = sp.playlist('spotify:playlist:4taxX9mVX4deBsqG6ffEbP')
        testing = playList.objects.get(pk=1).get_info()
        self.assertEqual(playlist, testing)

    def test_create_track(self):
        playlist = playList.objects.create(
            url='spotify:playlist:1mDavOft783W3vv8sgeo0B').create_track()
        song = songModel.objects.all().exists()
        self.assertTrue(song)

    def test_add_track_song_list(self):
        playlist = playList.objects.get(pk=1)
        playlist.add_track_song_list()
        qs = songModel.objects.filter(playlist__url=playlist.url).exists()
        self.assertTrue(qs)
        
