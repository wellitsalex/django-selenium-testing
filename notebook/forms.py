from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User
from .models import Note, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Enter your Email")
    username = forms.CharField(label="Create a username")

    class Meta:
        model = User
        fields = ("username", "email",)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        email_list = list(User.objects.values_list("email", flat=True))
        if email in email_list:
            raise ValidationError("Email is already in use")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) > 150:
            raise ValidationError("Username too long")
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Enter your username")

    class Meta:
        model = User
        fields = ("username", "password")


class EditForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "name": "Title"
    }))
    content = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
        "rows": 40,
        "cols": 100
    }))

    class Meta:
        model = Note
        fields = [
            "title",
            "content"
        ]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) >= 50:
            raise ValidationError("Title too large")
        elif len(title) == 0:
            raise ValidationError("Must provide a title")
        return title

    def clean_content(self):
        content = self.cleaned_data["content"]
        if len(content) >= 500:
            raise ValidationError("Content too large")
        return content


class UserForm(forms.ModelForm):
    #This does not prevent a user from editing the html still changing these values
    #my solution is just not saving this form, i.e nothing changes
    username = forms.CharField(disabled=True)
    date_joined = forms.CharField(disabled=True)
    email = forms.CharField(disabled=True)

    class Meta:
        model=User
        fields = ("username", "email", "date_joined",)


class UserProfileForm(forms.ModelForm):
    user_image = forms.ImageField(required=False)
    display_name = forms.CharField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ("display_name", "user_image",)