from distutils.log import error
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError, \
    JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .forms import AddPasswordForm, ShowPasswordForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
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

from .models import PasswordManager, PrivateKey

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .utils import derive_key, decrypt, encrypt, verify_master_password


class IndexView(LoginRequiredMixin, ListView):
    template_name = "password_manager/index.html"

    context_object_name = "passwords_list"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context["is_private_key_exists"] = PrivateKey.objects.filter(user=self.request.user).exists()
        return context

    def get_queryset(self):
        return PasswordManager.objects.filter(user=self.request.user).values("id", "title", "website_address", "login",
                                                                             "icon_name")


# def derive_key(password, salt):
#     kdf = PBKDF2(password, salt, 64, 1000)
#     key = kdf[:32]
#     return key


# def encrypt(user_master_password, social_password):
#     salt = get_random_bytes(AES.block_size)
#     private_key = derive_key(user_master_password, salt)
#
#     cipher_config = AES.new(private_key, AES.MODE_GCM)
#     cipher_text, tag = cipher_config.encrypt_and_digest(
#         bytes(social_password, "utf-8")
#     )
#
#     dictionary = {
#         'cipher_text': b64encode(cipher_text).decode('utf-8'),
#         'salt': b64encode(salt).decode('utf-8'),
#         'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
#         'tag': b64encode(tag).decode('utf-8')
#     }
#
#     return json.dumps(dictionary)


# def decrypt(encrypted_dict, user_master_password):
#     salt = b64decode(encrypted_dict["salt"])
#     cipher_text = b64decode(encrypted_dict["cipher_text"])
#     nonce = b64decode(encrypted_dict["nonce"])
#     tag = b64decode(encrypted_dict["tag"])
#
#     private_key = derive_key(user_master_password, salt)
#     cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
#
#     decrypted = cipher.decrypt_and_verify(cipher_text, tag)
#     return decrypted


# def verify_master_password(encrypted_dict, master_password):
#     try:
#         decrypt(encrypted_dict, master_password)
#         return True
#     except:
#         return False


exceptional_icons = {"stackoverflow": "stack-overflow",
                     "mastercard": "cc-mastercard",
                     "steamcommunity": "steam",
                     "stackexchange": "stack-exchange",
                     "visa": "cc-visa",
                     "mdbootstrap": "mdb",
                     "getbootstrap": "bootstrap",
                     "ok": "odnoklassniki",
                     "paypal": "cc-paypal",
                     "jcb": "cc-jcb", "discover": "cc-discover",
                     "americanexpress": "cc-amex",
                     "stripe": "cc-stripe", tuple(["pay", "amazon"]): "cc-amazon-pay"}


def get_domain_name(url):
    domain = urlparse(url).netloc.split(".")

    if exceptional_icons.get(tuple(domain)[0:2]) is not None:
        domain = exceptional_icons.get(tuple(domain)[0:2])

    elif len(domain) <= 2:
        if exceptional_icons.get(tuple(domain)[0]) is not None:
            domain = exceptional_icons.get(tuple(domain)[0])
        else:
            domain = domain[0]

    else:
        domain = domain[1]

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

            # print(PrivateKey.objects.get(user=request.user).private_key)

            if is_master_password_valid:
                decrypted_password = decrypt(
                    encrypted_dict, user_master_password).decode('utf-8')

                # print(decrypted_password)

                response = {
                    'password': decrypted_password,
                }

                return JsonResponse(response)

            else:

                return HttpResponseServerError("Master password is incorrect")

        return HttpResponseRedirect('/')


class AddNewPassword(generic.View):
    form_class = AddPasswordForm

    def post(self, request):

        form = AddPasswordForm(request.POST)

        if form.is_valid():

            password_object = form.save(commit=False)
            password_object.user = request.user
            print(password_object)

            password = request.POST.get("password")

            is_private_key_exists = PrivateKey.objects.filter(user=request.user).exists()

            salt = None

            if not request.POST.get("master_password") and is_private_key_exists:
                master_password = PrivateKey.objects.get(user=request.user).private_key
                salt = PrivateKey.objects.get(user=request.user).salt

            else:
                master_password = request.POST.get("master_password")

            password_object.encrypted_password = encrypt(
                master_password, password, salt)

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
        messages.success(request, "Password has been deleted successfully!")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


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

                new_password = encrypt(user_master_password, user_password, None)
                password.encrypted_password = new_password
                password.login = user_login
                password.title = user_title
                password.website_address = user_website
                password.icon_name = password_icon
                password.save()

            elif not user_password and user_master_password:

                user_current_social_password = decrypt(encrypted_password, user_confirm_password).decode("utf-8")
                new_password = encrypt(user_master_password, user_current_social_password, None)
                password.encrypted_password = new_password
                password.login = user_login
                password.title = user_title
                password.website_address = user_website
                password.icon_name = password_icon
                password.save()

            elif user_password and not user_master_password:

                new_password = encrypt(user_confirm_password, user_password, None)
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
                request, "Master password is incorrect. Try again!")
            return redirect("password_manager:index")


class ErrorHandler(TemplateView):
    template_name = "error/404.html"
