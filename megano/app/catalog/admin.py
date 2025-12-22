from django.contrib import admin

from .models import Category, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("src", "alt")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "indented_title", "parent")
    list_filter = ("parent",)
    search_fields = ("title",)

    def indented_title(self, obj):
        level = 0
        parent = obj.parent
        while parent:
            level += 1
            parent = parent.parent
        return "-" * level + " " + obj.title

    indented_title.short_description = "Category"
