
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from .forms import UserSignupForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic


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
