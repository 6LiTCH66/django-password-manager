
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import PasswordManager


class UpdatePasswordForm(forms.ModelForm):

    class Meta:
        model = PasswordManager
        fields = ["title", "website_address", "login"]


class ShowPasswordForm(forms.ModelForm):
    user_master_password = forms.CharField(max_length=255, required=True)

    class Meta:
        model = PasswordManager
        fields = ["user_master_password"]


class AddPasswordForm(forms.ModelForm):
    class Meta:
        model = PasswordManager
        fields = ["title", "login", "website_address"]


# class UserSignupForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         help_texts = {
#             'username': None,
#         }


# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ["username", "email", "first_name", "last_name"]


# class ProfileUpdateForm(forms.ModelForm):

#     class Meta:
#         model = Profile
#         fields = ['image']
