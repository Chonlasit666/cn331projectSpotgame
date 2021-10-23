from django.urls import path

from . import views

urlpatterns = [
    path('',views.about, name='aboutme'),
    path('contributors', views.contributors , name='contributors'),
]