from django.urls import path

from . import views
app_name = "smg"
urlpatterns = [
    path('', views.index, name='index'),
    path('(?P<room_name>\d+)/$', views.room, name='room'),
    path('aboutme/', views.about, name='aboutme'),
    path('createroom', views.create_room_view, name='createroom'),
]
