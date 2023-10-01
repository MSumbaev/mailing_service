from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    telegram = models.CharField(max_length=100, verbose_name='Telegram', **NULLABLE)
    verify_key = models.CharField(max_length=15, verbose_name='Ключ верификации', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

