from django.test import TestCase
from recipes.models import Profile;
from django.contrib.auth.models import User


"""
TEST SUMMARY

SETUP: 
    - create users1 and user2.
        - this should automatically create Profiles for each of the users
    - make user 1 follow user 2

TESTS:
    - check that on creation of user1 and user2 that a corresponding profile is made with correct name (2 tests, 1 per user)
    - check that user 1 follows 1 other user
    - check that user 2 follows no one
"""

class ProfileTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test1", password="password")
        User.objects.create(username="test2", password="password")
        Profile.objects.get(id=1).following.set([Profile.objects.get(id=2)])

    def test_automatic_profile_setup(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.name, "test1")
    
    def test_automatic_profile_setup_2(self):
        profile = Profile.objects.get(id=2)
        self.assertEqual(profile.name, "test2")

    def test_following_1(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.following.count(), 1)

    def test_following_2(self):
        profile = Profile.objects.get(id=2)
        self.assertEqual(profile.following.count(), 0)
        

