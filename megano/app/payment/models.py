from django.db import models

from app.order.models import Order


class Payment(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
        ]
    )
    createAt = models.DateTimeField(auto_now_add=True)
    transactionId = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Payment for order #{self.order}"
