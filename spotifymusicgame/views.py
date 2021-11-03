from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404,  redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import admin
from .models import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ffc4c1c607de49489dc5b071b326727e",
                                                           client_secret="4fd9dfe58f914768b24a034e1da88c2b"))


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


def createroom(request):
    data = []
    if request.method == "POST":
        a = request.POST['texttxt']
        if not playList.objects.filter(url=a).exists():
            playList.objects.create(url=a)
        data = ['test']
    else:
        data = ['Please,Input your track']

    return render(request, 'spotifymusicgame/createroom.html', {
        "data": data,
    }
    )
