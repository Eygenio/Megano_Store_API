from django.db import models

class Image(models.Model):
    """Модель Image - это модель ссылок на изображения,
        которые используются в интернет-магазине"""

    src = models.CharField(max_length=255)
    alt = models.CharField(max_length=255)

    def __str__(self):
        return self.src
