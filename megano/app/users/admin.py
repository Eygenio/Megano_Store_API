from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "email", "phone", "avatar")
    list_filter = ("fullname",)
    search_fields = ("fullname", "email", "phone")
