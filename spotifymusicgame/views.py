from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import json
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
    try:
        roomInfo.objects.get(id=room_name)
    except:
        return render(request, "spotifymusicgame/index.html")

    if not room_name.isdecimal():
        messages.info(request, 'Please enter valid room name')
        return render(request, "spotifymusicgame/index.html")
        
    current_user = roomInfo.objects.get(id=room_name).player_inroom
    max_user = roomInfo.objects.get(id=room_name).max_player
    is_playing = roomInfo.objects.get(id=room_name).is_playing
    # check if room full
    if(current_user >= max_user):
        messages.info(request, 'That room is already full')
        return render(request, "spotifymusicgame/index.html")
    # check if room playing
    if(is_playing):
        messages.info(request, 'That room is already playing')
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
                songs.append(str(i.song).replace("'", ""))
                artists.append(str(i.artist).replace("'", ""))
                images.append(str(i.image).replace("'", ""))
                uris.append(str(i.uri).replace("'", ""))

        for j in songModel.objects.all():
            dbsong.append(str(j.song).replace("'", ""))

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


def create_room_view(request):
    ID = None

    if request.method == "POST":
        try:

            URI_ = request.POST['URI']
            Max_player = request.POST['Max_player']
            if ((not URI_ or not Max_player) or not Max_player.isdecimal()) or (not ("spotify:playlist:") in URI_):
                if not Max_player:
                    messages.info(request, 'Please enter max player')
                elif not Max_player.isdecimal():
                    messages.info(request, 'Max player must be number')
                if not URI_:
                    messages.info(request, 'Please enter playlist URI')
                if not ("spotify:playlist:") in URI_:
                    messages.info(request, 'Please enter valid spotify playlist')
                return render(request, 'spotifymusicgame/createroom.html')

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
