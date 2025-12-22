from django.db import models

from app.users.models import User
from app.core.models import Image
from app.catalog.models import Product, Category, Tag


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True
        )
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    deliveryType = models.CharField(max_length=50)
    paymentType = models.CharField(max_length=50)
    totalCost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="products"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="(price * count)"
    )
    count = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    freeDelivery = models.BooleanField(default=False)
    images = models.ManyToManyField(Image, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    reviews = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
