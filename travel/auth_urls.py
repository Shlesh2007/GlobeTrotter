from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import StyledLoginForm
from . import views_auth

urlpatterns = [
    path("signup/", views_auth.sign_up, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="travel/auth/login.html",
            form_class=StyledLoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path(
        "password-reset/",
        views_auth.password_reset_request,
        name="password_reset",
    ),
    path(
        "password-reset/otp/",
        views_auth.password_reset_otp,
        name="password_reset_otp",
    ),
    path(
        "password-reset/new/",
        views_auth.password_reset_new,
        name="password_reset_new",
    ),
]
