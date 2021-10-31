from django.urls import path

from . import views
app_name = "spotifymusicgame"
urlpatterns = [
    path('spotifymusicgame/<int:room_name>/', views.room, name='room'),
    path('aboutme/',views.about, name='aboutme'),
    path('createroom',views.createroom,name='createroom')
]
