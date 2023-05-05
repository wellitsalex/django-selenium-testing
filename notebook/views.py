from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout

from .models import Note, UserProfile
from .forms import RegisterForm, LoginForm, EditForm, UserProfileForm, UserForm


class WelcomePageView(View):
    
    def get(self, request):
        return render(request, "notebook/index.html")


class LoginPageView(View):

    def get(self, request):

        context = {
            "login_form": LoginForm()
        }

        return render(request, "notebook/login.html", context)

    def post(slef, request):
        login_form = LoginForm(data=request.POST)

        context = {
            "login_form": login_form
        }

        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            #We know from .is_valid() that the user is already in the database and authenticated,
            #calling authenticate is an easy way to get that user data again to then login.
            user = authenticate(request, username=username, password=password)
            #session is created at login
            login(request, user)
            
            return HttpResponseRedirect(reverse("dashboard-page"))

        return render(request, "notebook/login.html", context)


class LogOutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("welcome-page"))
    

class PassResetView(PasswordResetView):
    template_name = "notebook/pass-reset.html"
    email_template_name = "notebook/pass-reset-email.html"
    subject_template_name = "notebook/pass-reset-sub.txt"

    #does all the heavy lifting for us!
    #Creates form, handles POST and sends email out based on template
    #also auto generates a uid and token for a secure url


class PassResetDoneView(View):

    def get(self, request):
        return render(request, "notebook/pass-reset-done.html")


class PassResetConfirm(PasswordResetConfirmView):
    template_name = "notebook/pass-reset-confirm.html"


class PassResetCompleteView(PasswordResetCompleteView):
    template_name = "notebook/pass-reset-complete.html"


class RegisterPageView(View):

    def get(self, request):

        context = {
            "register_form": RegisterForm()
        }

        return render(request, "notebook/register.html", context)

    def post(slef, request):
        register_form = RegisterForm(data=request.POST)

        context = {
            "register_form": register_form
        }

        if register_form.is_valid():
            register_form.save()

            #create the users profile 
            user_profile = UserProfile(
                user=User.objects.get(username=register_form.data["username"])
            )
            user_profile.save()

            return HttpResponseRedirect(reverse("login-page"))
        
        return render(request, "notebook/register.html", context)


class DashboardView(LoginRequiredMixin, View):
    login_url=reverse_lazy("login-page")
    redirect_field_name="dashboard-page"

    def get(self, request):
        user = request.user
        note_list = Note.objects.all().filter(author=user)
        user_profile = UserProfile.objects.get(user=user)

        context = {
            "user_notes": note_list,
            "display_name": user_profile.display_name,
            "user_image": user_profile.user_image
        }

        return render(request, "notebook/dashboard.html", context)


class AddNoteView(LoginRequiredMixin, View):
    login_url=reverse_lazy("login-page")
    redirect_field_name="dashboard-page"

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
    
        edit_form = EditForm()

        context = {
            "user_notes": Note.objects.all().filter(author=user),
            "edit_form": edit_form,
            "note_slug": None,
            "display_name": user_profile.display_name,
            "user_image": user_profile.user_image
        }

        return render(request, "notebook/edit-note.html", context)

    def post(self, request):
        #access the user and specific note we are creating
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        edit_form = EditForm(request.POST)

        if edit_form.is_valid():
        
            #create new note entry in database
            new_note = Note(
                title=edit_form.data["title"], 
                content=edit_form.data["content"], 
                author=user, 
                slug="temp"
            )
            new_note.save()

            #update slug
            new_note.slug=slugify(f"{edit_form.data['title']} {new_note.id}")
            new_note.save()

            #redirect to new slug url
            return HttpResponseRedirect(reverse("edit-note-page", args=[slugify(f"{edit_form.data['title']} {new_note.id}")]))
        
        context = {
            "user_notes": Note.objects.all().filter(author=user),
            "edit_form": edit_form,
            "note_slug": None,
            "display_name": user_profile.display_name,
            "user_image": user_profile.user_image
        }

        return render(request, "notebook/edit-note.html", context)


class DeleteNoteView(LoginRequiredMixin, View):
    login_url=reverse_lazy("login-page")
    redirect_field_name="dashboard-page"

    def get(self, request, note_slug):

        specific_note = Note.objects.get(slug=note_slug)
        specific_note.delete()

        return HttpResponseRedirect(reverse("dashboard-page"))


class SingleNoteView(LoginRequiredMixin, View):
    login_url=reverse_lazy("login-page")
    redirect_field_name="dashboard-page"

    def get(self, request, note_slug):
        #get user and note 
        user = request.user
        specific_note = Note.objects.get(slug=note_slug)
        user_profile = UserProfile.objects.get(user=user)

        # Make sure the correct user can see the note
        if user != specific_note.author:
            return HttpResponseRedirect(reverse("dashboard-page"))

        #prepopulate form with data
        edit_form = EditForm(instance=specific_note)

        context = {
            "user_notes": Note.objects.all().filter(author=user),
            "edit_form": edit_form,
            "note_slug": note_slug,
            "display_name": user_profile.display_name,
            "user_image": user_profile.user_image
        }

        return render(request, "notebook/edit-note.html", context)

    def post(slef, request, note_slug):
        #access the user and specific note we are editing
        user = request.user
        specific_note = Note.objects.get(slug=note_slug)
        user_profile = UserProfile.objects.get(user=user)

        # Make sure the correct user can edit the note
        if user != specific_note.author:
            return HttpResponseRedirect(reverse("dashboard-page"))

        #get the filled out form from post
        edit_form = EditForm(request.POST, instance=specific_note)

        #verify and create new slug (this happens even with no title change)
        if edit_form.is_valid():
            note_slug = slugify(f"{edit_form.data['title']} {specific_note.id}")
            edit_form.save()

            #update the note's slug with new title+id combo
            specific_note.slug = note_slug
            specific_note.save()

            #redirect to new slug url
            return HttpResponseRedirect(reverse("edit-note-page", args=[note_slug]))
        
        context = {
            "user_notes": Note.objects.all().filter(author=user),
            "edit_form": edit_form,
            "note_slug": note_slug,
            "display_name": user_profile.display_name,
            "user_image": user_profile.user_image
        }


        return render(request, "notebook/edit-note.html", context)


class UserProfilePageView(LoginRequiredMixin, View):
    login_url=reverse_lazy("login-page")
    redirect_field_name="profile-page"

    def get(self, request):
        user = request.user
        specific_user = User.objects.get(username=user)
        specific_profile = UserProfile.objects.get(user=user)

        user_profile_form = UserProfileForm(instance=specific_profile)
        user_form = UserForm(instance=specific_user)

        context = {
            "user_form": user_form,
            "user_profile_form": user_profile_form,
            "user_image":specific_profile.user_image
        }
        
        return render(request, "notebook/user-profile.html", context)

    def post(self, request):
        user = request.user
        specific_user = User.objects.get(username=user)
        specific_profile = UserProfile.objects.get(user=user)

        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=specific_profile)
        user_form = UserForm(instance=specific_user)

        if user_profile_form.is_valid():
            user_profile_form.save()

        context = {
            "user_form": user_form,
            "user_profile_form": user_profile_form,
            "user_image":specific_profile.user_image
        }
        
        return render(request, "notebook/user-profile.html", context)

