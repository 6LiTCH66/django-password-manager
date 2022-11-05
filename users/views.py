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


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print(form["username"].value())
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
            print("u_form is invalid")

        return render(request, self.template_name, {'u_form': u_form})

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
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


def derive_key(password, salt):
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key


class SetGlobalMasterPassword(generic.View):
    template_name = "user/profile.html"

    def post(self, request, user_id):
        master_key = request.POST['master_password']
        confirm_master_password = request.POST['confirm_master_password']

        if master_key == confirm_master_password:

            salt = get_random_bytes(AES.block_size)
            private_key = derive_key(master_key, salt)

            is_key_exists = PrivateKey.objects.filter(user__id=user_id).exists()
            if not is_key_exists:
                PrivateKey.objects.create(private_key=private_key, user_id=user_id)
            else:
                print("User with that key exists!")

            # send success message
        else:
            pass
            # send error message

        return redirect("users:profile")
