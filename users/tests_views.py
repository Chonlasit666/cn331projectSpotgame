from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .views import register_view


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        password = make_password('somepass@brave')
        User = get_user_model()
        user = User.objects.create(
            email="brave@test.com", username='brave', password=password)

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
        credentials = {'username': 'brave@test.com',
                       'password': 'somepass@brave'}
        response = self.client.post(
            reverse('users:login'), credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_warning_massage_login(self):
        credentials = {'username': 'brave@test.com',
                       'password': 'worngpassword'}
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


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = {
            'username': 'jj',
            'email': 'jj@test.com',
            'password1': '135798642Aa',
            'password2': '135798642Aa'
        }
        password = make_password('somepass@brave')
        User = get_user_model()
        User.objects.create(
            email="brave@test.com", username='brave', password=password)

    """
    Test view SignUp page
    """

    def test_autenticate_cant_view_register_view(self):
        self.client.login(username='brave@test.com', password='somepass@brave')
        response = self.client.get(reverse('users:register'))
        self.assertRedirects(response, reverse('smg:index'))

    def test_signup_page_url(self):
        response = self.client.get("/users/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/register.html')

    def test_can_register_user(self):
        response = self.client.post(
            '/users/register/', self.user, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_user_that_register_can_login(self):
        credentials = {'username': 'jj@test.com',
                       'password': '135798642Aa'}
        response = self.client.post(
            reverse('users:login'), credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_that_not_register_can_not_login(self):
        credentials = {'username': 'ololetmein@test.com',
                       'password': '1234567890'}
        response = self.client.post(
            reverse('users:login'), credentials, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid credential.')

    """
    Test passing context to form
    """

    def test_user_used_username(self):
        userusedusername = {
            'username': 'jj',
            'email': 'jj1@test.com',
            'password1': '135798642Aa',
            'password2': '135798642Aa'
        }
        response = self.client.post(
            '/users/register/', userusedusername, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_user_used_email(self):
        userusedemail = {
            'username': 'jj1',
            'email': 'jj@test.com',
            'password1': '135798642Aa',
            'password2': '135798642Aa'
        }
        response = self.client.post(
            '/users/register/', userusedemail, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_user_password_not_match(self):
        passwordnotmatch = {
            'username': 'jj2',
            'email': 'jj2@test.com',
            'password1': '123456789',
            'password2': '123456'
        }
        response = self.client.post(
            '/users/register/', passwordnotmatch, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_user_wrong_email_format(self):
        wrongemail = {
            'username': 'jj3',
            'email': 'jj2',
            'password1': '123456789',
            'password2': '123456789'
        }
        response = self.client.post(
            '/users/register/', wrongemail, format='text/html')
        self.assertEqual(response.status_code, 200)
