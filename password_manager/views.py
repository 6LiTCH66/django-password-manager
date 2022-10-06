
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from .forms import UserSignupForm, AddPasswordForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
import json


class IndexView(LoginRequiredMixin, ListView):
    template_name = "password_manager/index.html"

    def get_queryset(self):
        return None


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("password_manager:index")

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('password_manager:index')
        return super(CustomLoginView, self).get(*args, **kwargs)


class CustomSignupView(generic.CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy("password_manager:index")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('password_manager:index')
        return super(CustomSignupView, self).get(*args, **kwargs)


# def add_new_password(request):
#     print(request)
#     if request.method == "POST":
#         print("yess")

def derive_key(password, salt):
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key


def encrypt(user_master_password, social_password):
    salt = get_random_bytes(AES.block_size)
    private_key = derive_key(user_master_password, salt)

    cipher_config = AES.new(private_key, AES.MODE_GCM)
    cipher_text, tag = cipher_config.encrypt_and_digest(
        bytes(social_password, "utf-8"))

    dictionary = {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

    return json.dumps(dictionary)


class AddNewPassword(generic.View):
    form_class = AddPasswordForm

    def post(self, request):
        form = AddPasswordForm(request.POST)
        if form.is_valid():
            password_object = form.save(commit=False)
            password_object.user = request.user

            password = request.POST.get("password")
            master_password = request.POST.get("master_password")

            encrypted_password = encrypt(master_password, password)
            password_object.encrypted_password = encrypted_password
            password_object.save()

        return redirect('password_manager:index')
