from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = "accounts"


urlpatterns = [
    # path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),

    # path("login/", views.UserLoginView.as_view(), name="login"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
]
