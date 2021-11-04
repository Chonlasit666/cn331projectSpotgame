from django.urls import path

from . import views
app_name = "smg"
urlpatterns = [
    #path('(?P<room_id>[0-9]', views.room, name='room'),
    #path('int<room_name:id>', views.room, name='room'),
    path('(?P<room_name>\w+)/$', views.room, name='room'),
    path('aboutme/', views.about, name='aboutme'),
    path('createroom', views.create_room_view, name='createroom'),
]
