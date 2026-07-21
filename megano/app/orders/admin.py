from django.contrib import admin

from app.orders.models import DeliverySettings, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "createdAt",
        "fullName",
        "email",
        "phone",
        "deliveryType",
        "paymentType",
        "totalCost",
        "status",
        "city",
        "address",
    )
    list_filter = ("status", "city", "address", "totalCost")
    search_fields = ("fullName", "status", "city", "address")


@admin.register(DeliverySettings)
class DeliverySettingsAdmin(admin.ModelAdmin):
    DeliverySettings._meta.verbose_name_plural = "DeliverySettings"
    pass
