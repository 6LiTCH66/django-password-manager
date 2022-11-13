from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .forms import UserCreationForm, UserUpdateForm, ProfileUpdateForm, UserSignupForm
from password_manager.models import PasswordManager, PrivateKey
from django.views import generic
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
from password_manager.utils import derive_key


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():

            # print(form["username"].value())

            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("password_manager:index")
        else:
            messages.error(
                self.request,
                "Please enter a correct username and password. Note that both fields may be case-sensitive.")
            return render(self.request, "registration/login.html")

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

    def post(self, request):
        form = UserSignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("password_manager:index")

        else:
            error_dict = {}
            for field in form:
                for error in field.errors:
                    error_dict[field.label] = error

            messages.error(
                self.request, error_dict)
            return render(self.request, "registration/signup.html")

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('password_manager:index')
        return super(CustomSignupView, self).get(*args, **kwargs)


class ProfileView(TemplateView):
    template_name = "user/profile.html"

    def post(self, request, user_id):

        u_form = UserUpdateForm(self.request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            self.request.POST, self.request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            # add success message
            messages.success(
                request, "Your personal data has been changed successfully!")
            return redirect("users:profile")
        else:
            # same here but opposite message
            messages.error(request, "Your entered data is incorrect!")

        return redirect("users:profile")

    def get_context_data(self, *args, **kwargs):

        context = super(ProfileView, self).get_context_data(*args, **kwargs)

        context["is_private_key_exists"] = PrivateKey.objects.filter(user=self.request.user).exists()

        context['passwords'] = PasswordManager.objects.filter(
            user=self.request.user)

        context["u_form"] = UserUpdateForm(instance=self.request.user)
        context["p_form"] = ProfileUpdateForm(
            instance=self.request.user.profile)

        return context


class ChangePassword(generic.View):
    template_name = "user/profile.html"
    form_class = PasswordChangeForm

    def post(self, request, user_id):
        password_form = self.form_class(self.request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(self.request, password_form.user)

            messages.success(
                request, "Password has been changed successfully!")
            return redirect("password_manager:index")
        else:
            messages.error(request, "Primary password is incorrect!")
        # print(password_form.errors)
        # pass_form.errors => errore
        return redirect("users:profile")


class SetGlobalMasterPassword(generic.View):
    template_name = "user/profile.html"

    def post(self, request, user_id):

        if request.POST.get('master_password') and request.POST.get('confirm_master_password'):

            master_key = request.POST.get('master_password')
            confirm_master_password = request.POST.get('confirm_master_password')

            if master_key == confirm_master_password:

                salt = get_random_bytes(AES.block_size)
                private_key = derive_key(master_key, salt)

                is_key_exists = PrivateKey.objects.filter(user__id=user_id).exists()

                if not is_key_exists:
                    PrivateKey.objects.create(private_key=private_key, salt=salt, user_id=user_id)

                    messages.success(
                        request, "Global Master Password has been set successfully!")

                else:
                    messages.error(request, "User with Global Master Password already exists!")

            else:
                messages.error(request, "The two passwords don't match!")
        else:

            primary_master_password = request.POST.get("primary_master_password")
            new_master_password = request.POST.get("new_master_password")
            confirm_new_master_password = request.POST.get("confirm_new_master_password")

            if new_master_password == confirm_new_master_password:

                new_salt = get_random_bytes(AES.block_size)
                new_private_key = derive_key(new_master_password, new_salt)

                old_salt = PrivateKey.objects.get(user__id=user_id).salt
                old_private_key = derive_key(primary_master_password, old_salt)

                key_obj = PrivateKey.objects.get(private_key=old_private_key, user__id=user_id)
                key_obj.private_key = new_private_key
                key_obj.salt = new_salt
                key_obj.save()

                messages.success(request, "Your Master Password has been changed successfully!")
            else:
                messages.error(request, "Cannot update Global Master Password")

        return redirect("users:profile")
