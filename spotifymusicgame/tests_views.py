from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import roomInfo
from .views import *


class SpotifymusicgameTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        playlist = playList.objects.create(
            url='spotify:playlist:4taxX9mVX4deBsqG6ffEbP')
        room = roomInfo.objects.create(url=playlist, max_player=2)

        password = make_password('foo')
        User = get_user_model()
        user = User.objects.create(
            email="brave@test.com", username='brave', password=password)

    def test_unauthenticated_user_cannot_room_view(self):
        response = self.client.get(reverse('smg:room', args=(1,)))
        self.assertRedirects(response, reverse('users:login'))

    def test_aboutme(self):
        response = self.client.get(reverse('smg:aboutme'))
        self.assertEqual(response.status_code, 200)

    def test_with_true_condition_create_room(self):
        self.client.login(username='brave@test.com', password='foo')
        post_message = {
            'URI': 'spotify:playlist:1mDavOft783W3vv8sgeo0B',
            'Max_player': 2
        }
        response = self.client.post(
            reverse('smg:createroom'), post_message, follow=True)
        self.assertRedirects(response, reverse('smg:room', args=(2,)))

    def test_no_post_request_create_room(self):
        self.client.login(username='brave@test.com', password='foo')
        response = self.client.post(reverse('smg:createroom'), {}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_cannot_createroom(self):
        response = self.client.post(reverse('smg:createroom'), {}, follow=True)
        self.assertRedirects(response,'/users/login?next=/createroom')

    def test_just_view_with_auth(self):
        self.client.login(username='brave@test.com', password='foo')
        response = self.client.get(reverse('smg:createroom'))
        self.assertEqual(response.status_code, 200)
