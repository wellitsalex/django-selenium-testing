from django.test import TestCase

from django.contrib.auth.models import User


class UserTestCase(TestCase):

    def setUp(self):

        # Make sure database is clean
        self.assertFalse(User.objects.filter(username="testusername").exists())

        # Creates, saves, returns user
        User.objects.create_user("testusername", "test@test.com", "testpassword")

    def test_user_in_database(self):

        # Checking if user is in database
        self.assertTrue(User.objects.filter(username="testusername").exists())
        
    def test_create_user_data(self):

        # Get user object
        testUser = User.objects.get(username="testusername")

        # test data was set correctly
        self.assertEqual(testUser.username, "testusername")
        self.assertEqual(testUser.email, "test@test.com")
        self.assertTrue(testUser.check_password("testpassword"))

    def test_delete_user(self):

        # delete user
        User.objects.get(username="testusername").delete()

        # user deleted?
        self.assertFalse(User.objects.filter(username="testusername").exists())