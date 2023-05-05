from django.urls import path

from . import views

urlpatterns = [
    path("", views.WelcomePageView.as_view(), name="welcome-page"),

    path("register/", views.RegisterPageView.as_view(), name="register-page"),
    path("login/", views.LoginPageView.as_view(), name="login-page"),
    path("logout/", views.LogOutView.as_view(), name="logout-page"),

    path("reset/", views.PassResetView.as_view(), name="password_reset"),
    path("reset-done/", views.PassResetDoneView.as_view(), name="password_reset_done"),
    path("reset-confirm/<uidb64>/<token>/", views.PassResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset/complete/", views.PassResetCompleteView.as_view(), name="password_reset_complete"),

    path("dashboard/", views.DashboardView.as_view(), name="dashboard-page"),
    path("dashboard/add", views.AddNoteView.as_view(), name="add-note-page"),
    path("dashboard/delete/<slug:note_slug>/", views.DeleteNoteView.as_view(), name="delete-note-page"),
    path("dashboard/<slug:note_slug>/", views.SingleNoteView.as_view(), name="edit-note-page"),
    
    path("profile/", views.UserProfilePageView.as_view(), name="profile-page")
]