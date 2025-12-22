from rest_framework import serializers

from .models import Order, OrderItem
from app.catalog.serializers import ImageSerializer, TagSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(source="category_id")
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = (
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
            "products",
        )
