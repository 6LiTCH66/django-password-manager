from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

from password_manager.views import DeletePassword

app_name = "users"
urlpatterns = [
    path("signup/", views.CustomSignupView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("profile/", views.ProfileView.as_view(), name="profile"),

    path("profile/<int:password_id>/delete/",
         DeletePassword.as_view(), name="delete-profile-password"),
    path("profile/<int:user_id>/update",
         views.ProfileView.as_view(), name="update_profile"),
    path("profile/<int:user_id>/change-password",
         views.ChangePassword.as_view(), name="change_password"),
    path("profile/<int:user_id>/set-global-password", views.SetGlobalMasterPassword.as_view(),
         name="global_master_password")
]
