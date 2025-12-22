from django.db import models

class Image(models.Model):
    """Модель Image представляет изображение,
    для модели Category и User"""
    src = models.CharField(max_length=255)
    alt = models.CharField(max_length=255)

    def __str__(self):
        return self.src
