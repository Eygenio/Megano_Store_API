from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "my_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
    }
}