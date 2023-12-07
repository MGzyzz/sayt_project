from django.urls import path
from accounts.views import *

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/<int:id>/', DetailProfileView.as_view(), name='profile')
]