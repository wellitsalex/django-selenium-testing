from django.contrib import admin

from .models import Note, UserProfile

class NoteAdmin(admin.ModelAdmin):
    list_display=("title","author","date",)

class UserProfileAdmin(admin.ModelAdmin):
    list_display= ("user", "display_name")

admin.site.register(Note, NoteAdmin)
admin.site.register(UserProfile, UserProfileAdmin)