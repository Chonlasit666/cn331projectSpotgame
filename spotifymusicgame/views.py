from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse


import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ffc4c1c607de49489dc5b071b326727e",
                                                           client_secret="4fd9dfe58f914768b24a034e1da88c2b"))


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    else:
        return render(request, "spotifymusicgame/index.html")

def room(request, room_name):
    track = sp.track('spotify:track:6IG5ZOKnUryCcsvzopK23A')
    return render(request, 'spotifymusicgame/room.html', {
        'room_name': room_name,
        "name": track['name'],
        "artist": track['artists'][0]['name'],
        "pic": track['album']['images'][0]['url'],
        "url": track['preview_url'],
    })


def about(request):
    return render(request, 'spotifymusicgame/aboutme.html')


def create_room_view(request):
    ID = None
    if request.method == "POST":
        URI_ = request.POST['URI']
        Max_player = request.POST['Max_player']
        if not playList.objects.filter(url=URI_).exists():
            playList.objects.create(url=URI_)
        this_playlist = playList.objects.get(url = URI_)
        this_room = roomInfo.objects.create(url = this_playlist , max_player = Max_player)
        room_name = this_room.id
        return HttpResponseRedirect(reverse("smg:room", args = (room_name,)))

    return render(request, 'spotifymusicgame/createroom.html')





























def create_room_detial_view(request):
    """
    qs = songModel.objects.all()
    song_list = [{"artist": x.artist, "image": x.image, "song": x.song, "uri": x.uri} for x in qs]
    data = {
        "response": song_list
    }
    return JsonResponse(data)
    """
    data = {}
    if request.method == "POST":
        a = request.POST['texttxt']
        if not playList.objects.filter(url=a).exists():
            playList.objects.create(url=a)
        qs = songModel.objects.filter(playlist__url=a)
        song_list = [{"artist": x.artist, "image": x.image,
                      "song": x.song, "uri": x.uri} for x in qs]

        data = {
            "response": song_list
        }
        print(data)
    return render(request, 'spotifymusicgame/createroom.html',{
        "data": data
        }
    )
    """"""
