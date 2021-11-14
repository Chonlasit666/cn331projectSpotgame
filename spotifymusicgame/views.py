from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

import random
import json

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
    try:
        roomInfo.objects.get(id=room_name)
    except:
        return render(request, "spotifymusicgame/index.html")
    current_user = roomInfo.objects.get(id=room_name).player_inroom
    max_user = roomInfo.objects.get(id=room_name).max_player
    is_playing = roomInfo.objects.get(id=room_name).is_playing
    if(current_user >= max_user):
        return render(request, "spotifymusicgame/index.html")
    if(is_playing):
        return render(request, "spotifymusicgame/index.html")

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    else:
        songs = []
        artists = []
        images = []
        uris = []
        dbsong = []

        for i in songModel.objects.filter(playlist__url=roomInfo.objects.get(id=room_name).url):
            if not i.uri:
                pass
            else:
                songs.append(str(i.song).replace("'", "").replace(
                    "[", "").replace("]", "").replace('"', ''))
                artists.append(str(i.artist).replace("'", "").replace(
                    "[", "").replace("]", "").replace('"', ''))
                images.append(str(i.image).replace("'", "").replace(
                    "[", "").replace("]", "").replace('"', ''))
                uris.append(str(i.uri).replace("'", "").replace(
                    "[", "").replace("]", "").replace('"', ''))

        if len(songs) == 0:
            return render(request, "spotifymusicgame/index.html")

        for j in songModel.objects.all():
            dbsong.append(str(j.song).replace("'", "").replace(
                "[", "").replace("]", "").replace('"', ''))
        #print(songs)
        seed = room_name
        random.Random(seed).shuffle(songs)
        random.Random(seed).shuffle(artists)
        random.Random(seed).shuffle(images)
        random.Random(seed).shuffle(uris)

        song_json = json.dumps(songs)
        artist_json = json.dumps(artists)
        image_json = json.dumps(images)
        uri_json = json.dumps(uris)
        dbsong_json = json.dumps(dbsong)

        return render(request, 'spotifymusicgame/room.html', {
            'room_name': room_name,
            'songs': song_json,
            'artists': artist_json,
            'images': image_json,
            'uris': uri_json,
            'dbsong': dbsong_json,
        })


def about(request):
    return render(request, 'spotifymusicgame/aboutme.html')


@login_required(login_url='users:login')
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
            this_playlist = playList.objects.get(url=URI_)
            this_room = roomInfo.objects.create(
                url=this_playlist, max_player=Max_player)
            room_name = this_room.id
            return HttpResponseRedirect(reverse("smg:room", args=(room_name,)))

        except:
            return render(request, 'spotifymusicgame/createroom.html')

    return render(request, 'spotifymusicgame/createroom.html')
