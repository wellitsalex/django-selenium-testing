from django.test import TestCase

from notebook.models import UserProfile
from django.contrib.auth.models import User


class UserProfileTestCase(TestCase):

    def setUp(self):
        
        # Creates, saves, returns user
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")

        # Create a note entry 
        UserProfile.objects.create(user=testUser, display_name="test!")

    def test_user_profile_in_database(self):

        # Checking if note is in database

        self.assertTrue(UserProfile.objects.filter(user=User.objects.get(username="testusername")).exists())

    def test_user_profile_create(self):

        # Getting both objects
        testUser = User.objects.get(username="testusername")
        testUserProfile = UserProfile.objects.get(user=testUser)
        

        # Testing data fields
        self.assertEqual(testUserProfile.user, testUser)
        self.assertEqual(testUserProfile.display_name, "test!")
        self.assertFalse(testUserProfile.user_image)

    def test_user_profile_delete(self):

        # Delete note
        testUser = User.objects.get(username="testusername")
        UserProfile.objects.get(user=testUser).delete()
        
        self.assertFalse(UserProfile.objects.filter(user=testUser).exists())