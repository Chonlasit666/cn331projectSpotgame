from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
import random

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
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    else:
        songs = []
        artists = []
        images = []
        uris = []

        count = 0
        for i in songModel.objects.filter(playlist__url=roomInfo.objects.get(id = room_name).url):
            if not i.uri:
                pass
            else:
                songs.append(str(i.song).replace("'",""))
                artists.append(str(i.artist).replace("'",""))
                images.append(str(i.image).replace("'",""))
                uris.append(str(i.uri).replace("'",""))
        
        seed = random.randint(1,100)
        random.Random(seed).shuffle(songs)
        random.Random(seed).shuffle(artists)
        random.Random(seed).shuffle(images)
        random.Random(seed).shuffle(uris)

        song_json = json.dumps(songs)
        artist_json = json.dumps(artists)
        image_json = json.dumps(images)
        uri_json = json.dumps(uris)


        track = sp.track('spotify:track:6IG5ZOKnUryCcsvzopK23A')
        return render(request, 'spotifymusicgame/room.html', {
            'room_name': room_name,
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "pic": track['album']['images'][0]['url'],
            "url": track['preview_url'],
            'songs' : song_json,
            'artists' : artist_json,
            'images' : image_json,
            'uris' : uri_json,
        })


def about(request):
    return render(request, 'spotifymusicgame/aboutme.html')


def create_room_view(request):
    ID = None

    if request.method == "POST":
        try:

            URI_ = request.POST['URI']

            if not URI_:
                messages.info(request, 'Please enter playlist URI')
                return render(request, 'spotifymusicgame/createroom.html')

            Max_player = request.POST['Max_player']
            if not playList.objects.filter(url=URI_).exists():
                playList.objects.create(url=URI_)
            this_playlist = playList.objects.get(url = URI_)
            this_room = roomInfo.objects.create(url = this_playlist , max_player = Max_player)
            room_name = this_room.id
            return HttpResponseRedirect(reverse("smg:room", args = (room_name,)))

        except:
            return render(request, 'spotifymusicgame/createroom.html')

    return render(request, 'spotifymusicgame/createroom.html')



"""
def create_room_detial_view(request):
    
    qs = songModel.objects.all()
    song_list = [{"artist": x.artist, "image": x.image, "song": x.song, "uri": x.uri} for x in qs]
    data = {
        "response": song_list
    }
    return JsonResponse(data)
    
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
"""
