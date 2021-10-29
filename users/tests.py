from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import FriendList, FriendRequest


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com', username='normal', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNotNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='', username='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com', username='super', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNotNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', username='super', password='foo', is_superuser=False)


class UserModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com', username='normal', password='foo')

    def test_true_returns_user_model(self):
        user = get_user_model().objects.get(pk=1)
        self.assertEqual(user.email, str(user))

    def test_false_returns_user_model(self):
        user = get_user_model().objects.get(pk=1)
        self.assertNotEqual(user, str(user))


class FriendListTest(TestCase):

    def setUp(self):
        """
        Set up databases for testing FriendListModels
        u1 is friends with u2 and u2 also friends with u1 cause of many to many
        u3 have no friends
        """
        User = get_user_model()
        u1 = User.objects.create_user(
            email='u1@user.com', username='u1', password='foo')
        u2 = User.objects.create_user(
            email='u2@user.com', username='u2', password='foo')
        u3 = User.objects.create_user(
            email='u3@user.com', username='u3', password='foo')

        friendlistOne = FriendList.objects.create(user=u1)
        friendlistTwo = FriendList.objects.create(user=u2)
        friendlistThree = FriendList.objects.create(user=u3)
        friendlistOne.friends.add(u2)
        friendlistTwo.friends.add(u1)
        friendlistOne.save()
        friendlistTwo.save()

    """
        u stand for user
        fl stand for friendslist
    """

    def test_add_friend(self):
        """
        fl3 must increase
        """
        u1 = get_user_model().objects.get(pk=1)
        fl3 = FriendList.objects.get(pk=3)

        fl3.add_friend(u1)

        self.assertEqual(fl3.friends.count(), 1)

    def test_cannot_add_friend(self):
        """
        fl2 mustn't increase
        """
        u1 = get_user_model().objects.get(pk=1)
        fl2 = FriendList.objects.get(pk=2)

        fl2.add_friend(u1)

        self.assertNotEqual(fl2.friends.count(), 2)

    def test_remove_friend(self):
        """
        fl1 must be 0
        """
        u2 = get_user_model().objects.get(pk=2)
        fl1 = FriendList.objects.get(pk=1)

        fl1.remove_friend(u2)

        self.assertEqual(fl1.friends.count(), 0)

    def test_cannot_remove_friend(self):
        """
        fl1 doens't have any change
        """
        u3 = get_user_model().objects.get(pk=3)
        fl1 = FriendList.objects.get(pk=1)

        fl1.remove_friend(u3)

        self.assertEqual(fl1.friends.count(), 1)

    def test_unfriend(self):
        """
        initial number of friends in friendslistOne and friendslistTwo is 1
        after function unfriends number of friends in both list must be 0
        """
        fl1 = FriendList.objects.get(pk=1)
        self.assertEqual(fl1.friends.count(), 1)

        fl2 = FriendList.objects.get(pk=2)
        self.assertEqual(fl2.friends.count(), 1)

        u2 = get_user_model().objects.get(pk=2)

        fl1.unfriend(u2)

        fl2.refresh_from_db()

        self.assertEqual(fl1.friends.count(), 0)
        self.assertEqual(fl2.friends.count(), 0)

    def Test_cannot_unfriend(self):
        """
        friendlistOne mustn't have any change in it
        """
        fl1 = FriendList.objects.get(pk=1)
        u3 = get_user_model.objects.get(pk=3)

        fl1.unfriend(u3)
        self.assertNotEqual(fl1.friends.count(), 0)

    def Test_is_mutual_friend(self):
        """
        SAY YES THEY'RE FRIEND!!
        """
        fl1 = FriendList.objects.get(pk=1)
        u2 = get_user_model().objects.get(pk=2)

        self.assertTrue(fl1.is_mutual_friends(u2))
    
    def Test_is_not_mutual_friend(self):
        """
        SAY NO!!!
        """
        fl1 = FriendList.objects.get(pk=1)
        u3 = get_user_model().objects.get(pk=3)

        self.assertFalse(fl1.is_mutual_friends(u3))