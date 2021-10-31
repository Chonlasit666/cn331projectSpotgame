from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:room_name>/', views.room, name='room'),
    path('aboutme/',views.about, name='aboutme'),
]