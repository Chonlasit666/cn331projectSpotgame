from django.http.response import HttpResponseRedirect
from django.shortcuts import render , HttpResponse ,get_object_or_404  ,  redirect
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib import admin
from .models import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ffc4c1c607de49489dc5b071b326727e",
                                                           client_secret="4fd9dfe58f914768b24a034e1da88c2b"))

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
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

def login_view(request):
    if request.method == "POST":
        email = request.POST["username"]
        passw = request.POST["password"]
        user = authenticate(request , username=email, password = passw)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "spotifymusicgame/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "spotifymusicgame/login.html")

def logout_view(request):
    logout(request)
    return render(request, "spotifymusicgame/login.html",{
        "message" : "Logged out."
    })


def about(request):
    return render(request, 'spotifymusicgame/aboutme.html')

def createroom(request):
    data = []
    if request.method == "POST":
        a = request.POST['texttxt']
        try:
            a = playlist_uri['tracks']['items']
            count = 0
            playlistObj = {}
            for i in a:
                songObj = {
                "artist": i['track']['artists'][0]['name'],
                "image": i['track']['album']['images'][0]['url'],
                "song": i['track']['name'],
                "uri": i['track']['preview_url']
                }
                playlistObj[f"{count}"] = songObj
                count += 1
            print(playlistObj["2"]["song"])
        except:
            data = ['There are no data']
            
    else:
        data = ['Please,Input your track']
    
    return render(request,'spotifymusicgame/createroom.html',{
        "data" : data ,
    }
)