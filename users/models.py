from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=16)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Future Work Models May be in future we will use FriendSystem in our project to make a good exprerince for you
'''
class FriendList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,related_name='user')
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.user.email}"

    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """
        Remove a friend
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Initiate the action of unfriending someone
        """
        remover_friends_list = self  # THIS PERSON TERMINATE THE FRINEDSHIP

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove frined from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friends(self, friend):
        """
        Is this a friend?
        """
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    """
    Consists of two main parts:
        1. Sender
        2. Receiver
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.email

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
'''
