from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .forms import UserSignupForm, AddPasswordForm, ShowPasswordForm
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
from urllib.parse import urlparse

from .models import PasswordManager

from django.contrib import messages


class IndexView(LoginRequiredMixin, ListView):
    template_name = "password_manager/index.html"

    context_object_name = "passwords_list"

    def get_queryset(self):
        return PasswordManager.objects.filter(user=self.request.user).values("id", "title", "website_address", "login", "icon_name")


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


def decrypt(encrypted_dict, user_master_password):

    salt = b64decode(encrypted_dict["salt"])
    cipher_text = b64decode(encrypted_dict["cipher_text"])
    nonce = b64decode(encrypted_dict["nonce"])
    tag = b64decode(encrypted_dict["tag"])

    private_key = derive_key(user_master_password, salt)
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    return decrypted


def verify_master_password(encrypted_dict, master_password):
    try:
        decrypt(encrypted_dict, master_password)
        return True
    except:
        return False


# нужно сделать список для исключений типа stackoverflow => stack-overflow
def get_domain_name(url):
    domain = urlparse(url).netloc.split(".")

    if len(domain) >= 3:
        domain = domain[1]
    else:
        domain = domain[0]

    return domain


class ShowUserPassword(generic.View):

    def post(self, request):
        form = ShowPasswordForm(request.POST)
        if form.is_valid():
            password_id = request.POST.get("password_id")

            encrypted_dict = PasswordManager.objects.filter(
                user=request.user, pk=password_id).values("encrypted_password")[0]

            encrypted_dict = json.loads(
                encrypted_dict["encrypted_password"])

            user_master_password = request.POST.get("user_master_password")

            is_master_password_valid = verify_master_password(
                encrypted_dict, user_master_password)
            if is_master_password_valid:
                decrypted_password = decrypt(
                    encrypted_dict, user_master_password).decode('utf-8')
                print(decrypted_password)

                response = {
                    'password': decrypted_password,
                }

                return JsonResponse(response)

            else:

                return HttpResponseServerError("Master password is incorrect")

        return HttpResponseRedirect('/')


def add_new_password(request):
    if request.method == "POST":
        form = AddPasswordForm(request.POST)
        if form.is_valid():
            print(get_domain_name(request.POST.get("website_address")))

            password_object = form.save(commit=False)
            password_object.user = request.user

            password = request.POST.get("password")
            master_password = request.POST.get("master_password")

            # encrypted_password = encrypt(master_password, password)

            password_object.encrypted_password = encrypt(
                master_password, password)

            password_object.icon_name = get_domain_name(
                request.POST.get("website_address"))

            password_object.save()
            messages.success(request, "Password has been added successfully!")
        else:
            messages.error(request, "Fields cannot be empty.")
            return redirect('password_manager:index')

        return redirect('password_manager:index')


class AddNewPassword(generic.View):
    form_class = AddPasswordForm

    def post(self, request):
        form = AddPasswordForm(request.POST)
        if form.is_valid():
            print(get_domain_name(request.POST.get("website_address")))

            password_object = form.save(commit=False)
            password_object.user = request.user

            password = request.POST.get("password")
            master_password = request.POST.get("master_password")

            # encrypted_password = encrypt(master_password, password)

            password_object.encrypted_password = encrypt(
                master_password, password)

            password_object.icon_name = get_domain_name(
                request.POST.get("website_address"))

            password_object.save()
            messages.success(request, "Password has been added successfully!")
        else:
            messages.error(request, "Fields cannot be empty.")
            return redirect('password_manager:index')

        return redirect('password_manager:index')


class DeletePassword(generic.View):

    def get(self, request, password_id):
        password = get_object_or_404(PasswordManager, pk=password_id)
        password.delete()
        return redirect("password_manager:index")


class UpdatePassword(generic.View):

    def post(self, request, password_id):
        password = get_object_or_404(PasswordManager, pk=password_id)

        encrypted_password = password.encrypted_password
        user_title = request.POST["user_title"]
        user_login = request.POST["user_login"]
        user_password = request.POST["user_password"]
        user_master_password = request.POST["user_master_password"]
        user_website = request.POST["user_website"]
        user_confirm_password = request.POST["user_confirm_password"]
        password_icon = get_domain_name(user_website)

        encrypted_password = json.loads(
            encrypted_password)

        if verify_master_password(encrypted_password, user_confirm_password):

            if user_password and user_master_password:
                # нужно сделать проверку через decrypt потом
                new_password = encrypt(user_master_password, user_password)
                password.encrypted_password = new_password
                password.login = user_login
                password.title = user_title
                password.website_address = user_website
                password.icon_name = password_icon
                password.save()
            else:
                password.login = user_login
                password.title = user_title
                password.website_address = user_website
                password.icon_name = password_icon
                password.save()
            messages.success(
                request, "Password has been updated successfully!")
            return redirect("password_manager:index")

        else:
            messages.error(
                request, "Password has not been updated successfully!")
            return redirect("password_manager:index")
