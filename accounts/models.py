from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    description = models.CharField(max_length=350, verbose_name='Описание')
    status = models.BooleanField(default=True, verbose_name='Статус')
    email = models.EmailField(unique=True, verbose_name='Email')
    image = models.ImageField(upload_to='image')
    created_at = models.DateTimeField(auto_now_add=True)