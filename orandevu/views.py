from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import User
# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'

