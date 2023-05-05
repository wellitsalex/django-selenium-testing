from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateField(auto_now=True)
    content = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='images', null=True, blank=True)
    display_name = models.CharField(max_length=40, null=True, blank=True)
