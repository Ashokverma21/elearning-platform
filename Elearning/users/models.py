from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='profile_images/', default='default.png')

    def __str__(self):
        return self.user.username
