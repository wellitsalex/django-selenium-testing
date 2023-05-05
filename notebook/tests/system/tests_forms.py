from django.test import TestCase

from django.contrib.auth.models import User
from notebook.forms import RegisterForm, LoginForm, EditForm, UserProfileForm


class RegisterFormTest(TestCase):

    def test_valid_register_input(self):
        
        register_form = RegisterForm(data={
            "email": "test@test.com", 
            "username": "test", 
            "password1": "test1234!", 
            "password2": "test1234!"
        })

        self.assertEqual(register_form.errors, {})

    def test_invalid_register_input(self):

        # Adding a user to database
        User.objects.create_user("testusername", "test@test.com", "testpassword")
        
        # Testing bad email, existing username, empty password
        register_form = RegisterForm(data={
            "email": "testtest.com", 
            "username": "testusername", 
            "password1": "", 
            "password2": "test1234!"
        })

        self.assertEqual(register_form.errors["email"], ["Enter a valid email address."])
        self.assertEqual(register_form.errors["username"], ["A user with that username already exists."])
        self.assertEqual(register_form.errors["password1"], ["This field is required."])

        # Testing non matching passwords
        register_form2 = RegisterForm(data={
            "password1": "test12345!", 
            "password2": "test1234!"
        })

        self.assertEqual(register_form2.errors["password2"], ["The two password fields didn’t match."])

        # Testing username length, short/common passwords
        register_form3 = RegisterForm(data={
            "email": "test@test.com", 
            "username": 50*"test!",
            "password1": "zxcvbn", 
            "password2": "zxcvbn"
        })

        self.assertEqual(register_form3.errors["username"], ["Username too long"])
        self.assertEqual(register_form3.errors["password2"], ["This password is too short. It must contain at least 8 characters.",
                                                             "This password is too common."])

    def test_clean_register_email(self):

        User.objects.create_user("testusername", "test@test.com", "testpassword")

        register_form = RegisterForm(data={
            "email": "test@test.com",
        })

        self.assertEqual(register_form.errors["email"], ["Email is already in use"])


class LoginFormTest(TestCase):

    def test_valid_login_input(self):
        
        User.objects.create_user("testusername", "test@test.com", "testpassword")

        # Testing valid login
        login_form = LoginForm(data={
            "username" : "testusername",
            "password" : "testpassword" 
        })

        self.assertEqual(login_form.errors, {})

    def test_invalid_login_input(self):
        
        User.objects.create_user("testusername", "test@test.com", "testpassword")

        # Testing bad user/pass
        login_form = LoginForm(data={
            "username" : "testbad",
            "password" : "testbad" 
        })

        self.assertEqual(login_form.errors["__all__"], ["Please enter a correct username and password. Note that both fields may be case-sensitive."])

        # Testing empty user/pass
        login_form2 = LoginForm(data={
            "username" : "",
            "password" : "" 
        })

        self.assertEqual(login_form2.errors["username"], ["This field is required."])
        self.assertEqual(login_form2.errors["password"], ["This field is required."])

        # Testing bypass of max_char limit
        login_form3 = LoginForm(data={
            "username": 50*"test!",
            "password": "password"
        })

        self.assertEqual(login_form3.errors["__all__"], ["Please enter a correct username and password. Note that both fields may be case-sensitive."])


class EditFormTest(TestCase):
    
    def test_valid_edit_input(self):
        
        # Testing valid edit form 
        edit_form = EditForm(data={
            "title": "note1",
            "content": "some text"
        })

        self.assertEqual(edit_form.errors, {})

    def test_invalid_edit_input(self):

        # Testing bad title/content length 
        edit_form = EditForm(data={
            "title": 50*"test!",
            "content": 101*"test!"
        })

        self.assertEqual(edit_form.errors["title"], ["Ensure this value has at most 50 characters (it has 250)."])
        self.assertEqual(edit_form.errors["content"], ["Ensure this value has at most 500 characters (it has 505)."])

        edit_form2 = EditForm(data={
            "title": "",
            "content": "Some content"
        })

        self.assertEqual(edit_form2.errors["title"], ["This field is required."])


class UserProfileFormTest(TestCase):
    
    def test_valid_user_profile_input(self):
        
        user_profile_form = UserProfileForm(data={
            "display_name" : "",
            "user_image" : "",
        })

        self.assertEqual(user_profile_form.errors, {})

    def test_invalid_user_profile_input(self):

        user_profile_form = UserProfileForm(data={
            "display_name" : 50*"test!",
            "user_image" : "",
        })

        self.assertEqual(user_profile_form.errors["display_name"], ["Ensure this value has at most 40 characters (it has 250)."])