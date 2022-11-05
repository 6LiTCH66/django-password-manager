from django.contrib import admin
from .models import PasswordManager, PrivateKey

admin.site.register(PasswordManager)
admin.site.register(PrivateKey)
# admin.site.register(Profile)
