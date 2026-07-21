from django.db import models


class Image(models.Model):
    src = models.CharField(max_length=255)
    alt = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.src
