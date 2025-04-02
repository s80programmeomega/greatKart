from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import UserLoginForm, UserSignUpForm


class UserRegisterView(View):

    def get(self, request: HttpRequest):
        return render(request, 'accounts/register.html')

    def post(self, request: HttpRequest):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user_model = get_user_model()
            user_model.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'),
            )
            messages.success(request,
                             'Account created successfully',
                             extra_tags='success')
            return redirect('accounts:login')
        else:
            context = {'form': form}
            messages.error(request,
                           'Invalid form submission',
                           extra_tags='danger')
            print(form.errors)
            return render(request, 'accounts/register.html', context=context)


class UserLoginView(UserPassesTestMixin, View):

    def test_func(self):
        # Allow access only if the user is not authenticated
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        # Redirect authenticated users to the home page (or another page)
        return redirect('home')

    def get(self, request: HttpRequest):
        form = UserLoginForm()
        context = {'form': form}
        # Render the login page for GET requests
        return render(request, 'accounts/login.html', context=context)

    def post(self, request: HttpRequest):
        # Handle login logic for POST requests
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request,
                               'Invalid login credentials',
                               extra_tags='danger')
        context = {'form': form}
        return render(request, 'accounts/login.html', context=context)


def user_is_logged_out(user: User):
    return not user.is_authenticated


@user_passes_test(user_is_logged_out, login_url='home')
def user_login(request: HttpRequest):
    # if request.user.is_authenticated:
    #     # Redirect authenticated users to the previous page or fallback to 'home'
    #     previous_url = request.META.get('HTTP_REFERER', 'home')
    #     return redirect(previous_url)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            auth_login(request, user)
            # Redirect to the 'next' parameter if it exists, otherwise go to the home page
            # 'home' is the fallback URL name
            next_url = request.GET.get('next', "home")
            return redirect(next_url)
        else:
            messages.error(request,
                           'Invalid login credentials',
                           extra_tags='danger')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')


def user_logout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'accounts/logout.html')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    # Redirect to login page after logout
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        # Log out the user after a successful password change
        _ = super().form_valid(form)
        logout(self.request)
        return redirect(self.success_url)
