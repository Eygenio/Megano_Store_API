from django.contrib import admin

from app.core.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("src", "alt")
