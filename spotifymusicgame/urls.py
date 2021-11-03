from django.urls import path

from . import views
app_name = "smg"
urlpatterns = [
    path('spotifymusicgame/<int:room_name>/', views.room, name='room'),
    path('aboutme/', views.about, name='aboutme'),
    path('createroom', views.create_room_view, name='createroom'),
    path('createroom/detial', views.create_room_detial_view,
         name='create_room_detial')
]
