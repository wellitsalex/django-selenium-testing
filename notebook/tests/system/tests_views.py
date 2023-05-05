from django.test import TestCase
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from notebook.models import Note, UserProfile

from django.contrib.auth import get_user

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class WelcomePageViewTest(TestCase):

    def test_welcome_get(self):
        # Can we see the page
        response = self.client.get(reverse_lazy("welcome-page"))
        self.assertEqual(response.status_code, 200)


class LoginPageViewTest(TestCase):
    
    def test_login_get(self):

        # Can we see the page and login form
        response = self.client.get(reverse_lazy("login-page"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["login_form"])

    def test_login_post_invalid_user(self):

        response = self.client.post(reverse_lazy("login-page"), username='testuser', password='testpass')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_login_post_valid_user(self):

        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)

        login_data = {
            "username" :"testusername",
            "password" :"testpassword"
        }

        response = self.client.post(reverse_lazy("login-page"), login_data)

        self.assertTrue(get_user(self.client).is_authenticated)
        self.assertRedirects(response, reverse_lazy("dashboard-page"))


class LogoutViewTest(TestCase):

    def setUp(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        self.client.login(username="testusername", password="testpassword")

    def test_logout_get(self):

        self.assertTrue(get_user(self.client).is_authenticated)

        self.client.get(reverse_lazy("logout-page"))

        self.assertFalse(get_user(self.client).is_authenticated)


class RegisterPageViewTest(TestCase):

    def test_register_get(self):
        response = self.client.get(reverse_lazy("register-page"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["register_form"])

    def test_register_post_valid(self):
        
        register_data = {
            "username": "testusername",
            "email": "test@test.com",
            "password1": "loginpass!",
            "password2": "loginpass!"
        }

        response = self.client.post(reverse_lazy("register-page"), register_data)
        
        self.assertRedirects(response, reverse_lazy("login-page"))

    def test_register_post_duplicate_user(self):

        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)

        # data that already exists 
        register_data = {
            "username": "testusername",
            "email": "test@test.com",
            "password1": "loginpass!",
            "password2": "loginpass!"
        }

        response = self.client.post(reverse_lazy("register-page"), register_data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["register_form"])


class DashboardViewTest(TestCase):

    def test_dashboard_unauth_get(self):
        # Can we can't see the page un-authed

        response = self.client.get(reverse_lazy("dashboard-page"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?dashboard-page=/dashboard/")

    def test_dashboard_auth_get(self):
        
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)
        
        self.client.force_login(testUser)

        response = self.client.get(reverse_lazy("dashboard-page"))

        self.assertEqual(response.status_code, 200)


class PassResetViewTest(TestCase):

    def test_passreset_get(self):

        response = self.client.get(reverse_lazy("password_reset"))
        self.assertEqual(response.status_code, 200)

    def test_passreset_email_valid_post(self):

        reset_data = {
            "email": "test@test.com"
        }

        response = self.client.post(reverse_lazy("password_reset"), reset_data)

        self.assertRedirects(response, reverse_lazy("password_reset_done"))

    def test_passreset_email_invalid_post(self):

        reset_data = {
            "email": "testtest"
        }

        response = self.client.post(reverse_lazy("password_reset"), reset_data)

        self.assertEqual(response.status_code, 200)


class PassResetDoneViewTest(TestCase):

    def test_passreset_done_get(self):

        response = self.client.get(reverse_lazy("password_reset_done"))
        self.assertEqual(response.status_code, 200)


class PassResetConfirmViewTest(TestCase):

    def setUp(self):
        
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)

        self.uid = urlsafe_base64_encode(force_bytes(testUser.pk))
        self.token = default_token_generator.make_token(testUser)

        self.url = f"/reset-confirm/{self.uid}/{self.token}/"

    def test_passreset_confirm_get(self):

        response = self.client.get(self.url)
        self.assertRedirects(response, f"/reset-confirm/{self.uid}/set-password/")

    def test_passreset_confirm_valid_post(self):

        self.url = f"/reset-confirm/{self.uid}/set-password/"

        reset_data = {
            "new_password1": "pass123test!",
            "new_password2": "pass123test!"
        }

        session = self.client.session
        session['_password_reset_token'] = self.token
        session.save()

        response = self.client.post(self.url, reset_data)
        self.assertRedirects(response, reverse_lazy("password_reset_complete"))

    def test_passreset_confirm_invalid_post(self):

        self.url = f"/reset-confirm/{self.uid}/set-password/"

        reset_data = {
            "new_password1": "pass123test!",
            "new_password2": "passtest!"
        }

        response = self.client.post(self.url, reset_data)
        self.assertEqual(response.status_code, 200)


class PassResetCompleteViewTest(TestCase):

    def test_passreset_complete_get(self):

        response = self.client.get(reverse_lazy("password_reset_complete"))
        self.assertEqual(response.status_code, 200)


class AddNoteViewTest(TestCase):
    
    def test_addnote_unauth_get(self):
    
        response = self.client.get(reverse_lazy("add-note-page"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?dashboard-page=/dashboard/add")

    def test_addnote_auth_get(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)

        self.client.force_login(testUser)

        response = self.client.get(reverse_lazy("add-note-page"))

        self.assertEqual(response.status_code, 200)
     
    def test_addnote_valid_post(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)

        self.client.force_login(testUser)
        
        note_data = {
            "title": "Valid Title",
            "content": "More valid content"
        }

        response = self.client.post(reverse_lazy("add-note-page"), note_data)

        self.assertRedirects(response, "/dashboard/valid-title-5/")

    def test_addnote_invalid_post(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)

        self.client.force_login(testUser)

        note_data = {
            "title": "",
            "content": "More valid content"
        }

        response = self.client.post(reverse_lazy("add-note-page"), note_data)

        self.assertEqual(response.status_code, 200)


class DeleteNoteViewTest(TestCase):

    def test_deletenote_unauth_get(self):
        
        response = self.client.get("/dashboard/delete/valid-title-1/")
        self.assertRedirects(response, "/login/?dashboard-page=/dashboard/delete/valid-title-1/")

    def test_deletenote_auth_get(self):

        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)
        self.client.force_login(testUser)
        
        note_data = {
            "title": "Valid Title2",
            "content": "More valid content2"
        }

        response = self.client.post(reverse_lazy("add-note-page"), note_data)
        self.assertRedirects(response, "/dashboard/valid-title2-6/")

        response = self.client.get("/dashboard/delete/valid-title2-6/")
        self.assertRedirects(response, reverse_lazy("dashboard-page"))


class SingleNoteViewTest(TestCase):

    def test_singlenote_unauth_get(self):
        response = self.client.get("/dashboard/valid-title-1/")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?dashboard-page=/dashboard/valid-title-1/")

    def test_singlenote_auth_get(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)
        self.client.force_login(testUser)

        # Create note
        note_data = {
            "title": "Valid Titled",
            "content": "More valid content"
        }
        response = self.client.post(reverse_lazy("add-note-page"), note_data)
        self.assertRedirects(response, "/dashboard/valid-titled-8/")

        # Redirect to dashboard, then back to note
        response = self.client.get(reverse_lazy("dashboard-page"))
        self.assertEqual(response.status_code, 200)

        # Now visit single note page
        response = self.client.get("/dashboard/valid-titled-8/")
        self.assertEqual(response.status_code, 200)

    def test_singlenote_invalid_post(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)

        self.client.force_login(testUser)

        # Create note
        note_data = {
            "title": "Valid Titled",
            "content": "More valid content"
        }
        response = self.client.post(reverse_lazy("add-note-page"), note_data)
        self.assertRedirects(response, "/dashboard/valid-titled-9/")
        
        # Edit note 
        note_data = {
            "title": "",
            "content": "More valid content"
        }

        response = self.client.post("/dashboard/valid-titled-9/", note_data)
        self.assertEqual(response.status_code, 200)

    def test_singlenote_valid_post(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)

        self.client.force_login(testUser)

        # Create note
        note_data = {
            "title": "Valid Titled",
            "content": "More valid content"
        }
        response = self.client.post(reverse_lazy("add-note-page"), note_data)
        self.assertRedirects(response, "/dashboard/valid-titled-10/")
        
        # Edit note
        note_data = {
            "title": "Valid Title2",
            "content": "More valid content"
        }

        response = self.client.post("/dashboard/valid-titled-10/", note_data)
        self.assertRedirects(response, "/dashboard/valid-title2-10/")

    def test_correct_user_get(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)
        self.client.force_login(testUser)

        # Create note with user "testUser"
        note_data = {
            "title": "Valid Titled",
            "content": "More valid content"
        }
        response = self.client.post(reverse_lazy("add-note-page"), note_data)
        self.assertRedirects(response, "/dashboard/valid-titled-7/")

        # Logout the user who made the note
        self.client.logout()

        #Create new bad user
        badUser = User.objects.create_user("badusername", "test2@test.com", "testpassword")
        UserProfile.objects.create(user=badUser)
        self.client.force_login(badUser)

        # Atempt to access note by different user redirected to dashboard instead
        response = self.client.get("/dashboard/valid-titled-7/")
        self.assertRedirects(response, reverse_lazy("dashboard-page"))


class UserProfilePageViewTest(TestCase):

    def test_userprofile_unauth_get(self):
        response = self.client.get("/profile/")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?profile-page=/profile/")

    def test_userprofile_auth_get(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)
        self.client.force_login(testUser)

        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)

    def test_userprofile_post(self):
        testUser = User.objects.create_user("testusername", "test@test.com", "testpassword")
        UserProfile.objects.create(user=testUser)
        self.client.force_login(testUser)

        userprofile_data = {
            "display_name": "test",
            "user_image": "test.jpg"
        }

        response = self.client.post("/profile/", userprofile_data)
        self.assertEqual(response.status_code, 200)