from django.contrib.auth.models import AbstractUser
from django.db import models

from app.core.models import Image


class User(AbstractUser):
    """Модель User - это модель пользователя,
        которые зарегистрированы в интернет-магазине"""

    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    avatar = models.OneToOneField(
        Image,
        on_delete=models.CASCADE,
        related_name="avatar",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.fullname