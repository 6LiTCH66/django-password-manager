from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "password_manager"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("add/", views.AddNewPassword.as_view(), name="add"),
    path("show/", views.ShowUserPassword.as_view(), name="show"),
    path("signup/", views.CustomSignupView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
