from django.db import models
from django.contrib.auth.models import User


class PrivateKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    private_key = models.BinaryField()
    salt = models.BinaryField()

    def __str__(self):
        return str(self.user)


class PasswordManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    website_address = models.URLField()
    encrypted_password = models.JSONField()
    login = models.CharField(max_length=150)
    icon_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title
