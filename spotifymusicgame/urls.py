from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutme/',views.about, name='aboutme'),
]