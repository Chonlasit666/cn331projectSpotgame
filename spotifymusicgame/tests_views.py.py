from django.test import TestCase, Client
from django.urls import reverse

class SpotifymusicgameTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_unauthenticated_user_cannot_room_view(self):
        response = self.client.get(reverse('smg:room'))
        self.assertRedirects(response, reverse('users:login'))

