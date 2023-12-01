from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView
from accounts.models import User
from accounts.forms import LoginForm, RegisterForm
# Create your views here.


class LoginUserView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm


class LogoutUserView(LogoutView):
    def get_next_page(self):
        return self.request.META.get('HTTP_REFERER')


class RegisterUserView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')