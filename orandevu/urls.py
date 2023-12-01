from django.urls import path
from orandevu.views import *

urlpatterns = [
    path('', Home.as_view(), name='home')
]