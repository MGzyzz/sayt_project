from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from accounts.models import User
from accounts.forms import LoginForm, RegisterForm
# Create your views here.


class LoginUserView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse('home')


class LogoutUserView(LogoutView):
    def get_next_page(self):
        return self.request.META.get('HTTP_REFERER')


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        print(form.errors)
        user = form.save()
        login(self.request, user)
        return redirect('home')


class DetailProfileView(DetailView):
    template_name = 'registration/detailProfileView.html'
    model = User
    pk_url_kwarg = 'id'


