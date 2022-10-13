from contextlib import nullcontext
from email.policy import default

from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class PasswordManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    website_address = models.URLField()
    encrypted_password = models.JSONField()
    login = models.CharField(max_length=150)
    icon_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="anonymous_user.jpeg")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
