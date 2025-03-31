from django.contrib import messages
from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.auth import login as auth_login
from django.http import HttpRequest
from django.shortcuts import redirect, render
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
            messages.success(request, 'Account created successfully',
                             extra_tags='success')
            return redirect('accounts:login')
        else:
            context = {'form': form}
            messages.error(request, 'Invalid form submission',
                           extra_tags='danger')
            print(form.errors)
            return render(request, 'accounts/register.html', context=context)


class UserLoginView(View):
    def get(self, request: HttpRequest):
        form = UserLoginForm()
        context = {'form': form}
        # Render the login page for GET requests
        return render(request, 'accounts/login.html', context=context)

    def post(self, request: HttpRequest):
        # Handle login logic for POST requests
        form = UserLoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.data)
            email = form.data.get('email')
            password = form.data.get('password')

            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                # Redirect to the 'next' parameter if it exists, otherwise go to the home page
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid login credentials',
                               extra_tags='danger')
                context = {'form': form}
                return render(request=request, template_name='accounts/login.html', context=context)
        else:
            context = {'form': form}
            return render(request=request, template_name='accounts/login.html', context=context)


def user_login(request: HttpRequest):
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
            messages.error(request, 'Invalid login credentials',
                           extra_tags='danger')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')


def user_logout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'accounts/logout.html')
