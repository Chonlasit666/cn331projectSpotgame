from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        password = make_password('somepass@brave')
        User = get_user_model()
        user = User.objects.create(email="brave@test.com",username='brave', password=password)

    def test_guest_index_view(self):
        response = self.client.get(reverse('smg:index'))
        self.assertRedirects(response, reverse('users:login'))

    def test_authenticated_user_index_view(self):
        self.client.login(username='brave@test.com', password='somepass@brave')

        response = self.client.get(reverse('smg:index'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_can_login(self):
        credentials = {'username': 'brave@test.com', 'password': 'somepass@brave'}
        response = self.client.post(
            reverse('users:login'), credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_warning_massage_login(self):
        credentials = {'username': 'brave@test.com', 'password': 'worngpassword'}
        response = self.client.post(
            reverse('users:login'), credentials, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid credential.')

    def test_logout_view(self):
        self.client.login(username='brave@test.com', password='somepass@brave')
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)

    def test_success_massage_logout(self):
        self.client.login(username='brave@test.com', password='somepass@brave')
        response = self.client.post(reverse('users:logout'))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Logged out.')
