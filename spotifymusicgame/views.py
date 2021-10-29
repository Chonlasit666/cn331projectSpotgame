from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ffc4c1c607de49489dc5b071b326727e",
                                               client_secret="4fd9dfe58f914768b24a034e1da88c2b",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))


# Create your views here.
def index(request):
    track = sp.track('spotify:track:6IG5ZOKnUryCcsvzopK23A')
    print(track['artists'][0]['name'])
    return render(request, 'spotifymusicgame/index.html',{
        "name" : track['name'],
        "artist" : track['artists'][0]['name'],
        "pic" : track['album']['images'][0]['url'],
        "url" : track['preview_url'] ,
        
    })

def about(request):
    return render(request, 'spotifymusicgame/aboutme.html')