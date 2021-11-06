from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def login_view(request):
    if request.method == "POST":
        email = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('smg:index'))
        else:
            messages.warning(request, "Invalid credential.")
            return render(request, "users/login.html", {
                "messages": messages.get_messages(request)
            })

    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
    return render(request, "users/login.html", {
        "messages": messages.get_messages(request)
    })
