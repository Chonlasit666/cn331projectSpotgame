from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('spotifymusicgame/<int:room_name>/', views.room, name='room'),
    path('aboutme/',views.about, name='aboutme'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view , name = 'logout'),
]