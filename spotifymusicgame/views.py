from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ffc4c1c607de49489dc5b071b326727e",
                                                           client_secret="4fd9dfe58f914768b24a034e1da88c2b"))

def index(request):
    return render(request, 'spotifymusicgame/index.html', {})

def room(request, room_name):
    track = sp.track('spotify:track:6IG5ZOKnUryCcsvzopK23A')
    return render(request, 'spotifymusicgame/room.html', {
        'room_name': room_name,
        "name" : track['name'],
        "artist" : track['artists'][0]['name'],
        "pic" : track['album']['images'][0]['url'],
        "url" : track['preview_url'] ,
    })

def about(request):
    return render(request, 'spotifymusicgame/aboutme.html')