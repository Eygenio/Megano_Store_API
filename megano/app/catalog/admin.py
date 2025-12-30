from django.contrib import admin

from .models import Category, Tag, Review, Specification, Product, Sales


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "indented_title", "parent", "image")
    list_display_links = ("id", "indented_title")
    ordering = ("title", "parent")
    search_fields = ("title",)
    Category._meta.verbose_name_plural = "Categories"

    def indented_title(self, obj):
        level = 0
        parent = obj.parent
        while parent:
            level += 1
            parent = parent.parent
        return "-" * level + " " + obj.title

    indented_title.short_description = "category"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "author", "text_short", "rate", "date")
    search_fields = ("product", "author", "text", "rate", "date")

    def text_short(self, obj: Review) -> str:
        if len(obj.text) < 50:
            return obj.text
        return obj.text[:50] + "..."


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value")
    search_fields = ("name", "value")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "price",
        "count",
        "rating",
        "freeDelivery",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "category")


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        "product__id",
        "product__title",
        "product__category",
        "product__price",
        "salePrice",
        "product__count",
        "product__rating",
    )
    list_filter = (
        "product__title",
        "product__category",
        "product__count",
        "product__rating",
    )
    search_fields = ("product__title", "product__category")
    Sales._meta.verbose_name_plural = "Sales"
