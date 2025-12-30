from django.db import models

from app.catalog.models import Product
from app.users.models import User


class Basket(models.Model):
    """
    Модель "корзины" в интернет-магазине.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="basket",
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="basket_items"
    )
    count = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="(product.price * count)"
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} x {self.count}"
