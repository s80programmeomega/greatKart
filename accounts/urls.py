from . import views
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

app_name = "accounts"


urlpatterns = [
    # path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),

    # path("login/", views.UserLoginView.as_view(), name="login"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),

    # Password reset views
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html", email_template_name="accounts/password_reset_email.html",
        success_url=reverse_lazy("accounts:password_reset_done"), extra_email_context={
            'domain': 'localhost:8000',  # Use localhost for development
            'protocol': 'http',  # Use http for local development
        }), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url=reverse_lazy("accounts:password_reset_complete")), name="password_reset_confirm"),
    path("reset_done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]
