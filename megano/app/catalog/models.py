from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from app.core.models import Image
from app.users.models import User


class Category(models.Model):
    """Модель Category - это модель категорий товаров,
    которые представлены в интернет-магазине"""

    title = models.CharField(max_length=255)
    image = models.OneToOneField(
        Image,
        on_delete=models.CASCADE,
        related_name="category",
        null=True,
        blank=True
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Модель Tag - это модель "тэгов" товаров,
        которые представлены в интернет-магазине"""

    name = models.CharField(max_length=255, unique=True)


class Review(models.Model):
    """Модель Review - это модель отзывов на товары,
        которые представлены в интернет-магазине"""

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="review_list"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="reviews",
        null=True,
        blank=True
    )
    author = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.CharField(max_length=1000, blank=True, null=True)
    rate = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} ({self.rate})"


class Specification(models.Model):
    """Модель Specification - это модель характеристик товаров,
        которые представлены в интернет-магазине"""

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="specifications"
    )
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Product(models.Model):
    """Модель Product - это модель товаров,
        которые представлены в интернет-магазине"""

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    fullDescription = models.TextField(blank=True, null=True)
    freeDelivery = models.BooleanField(default=False)
    images = models.ManyToManyField(
        Image,
        related_name="products",
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="products",
        blank=True,
    )
    reviews = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0
    )
    sortIndex = models.IntegerField(default=0)
    purchases = models.IntegerField(default=0)
    limited = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Sales(models.Model):
    """Модель Sales - это модель скидки на товары,
        которые представлены в интернет-магазине"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sales"
    )
    salePrice = models.DecimalField(max_digits=10, decimal_places=2)
    dateFrom = models.DateField()
    dateTo = models.DateField()
