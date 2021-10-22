from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contributors', views.contributors , name='contributors'),
    path('aboutme',views.about, name='aboutme'),
]