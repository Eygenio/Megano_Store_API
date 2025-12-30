from rest_framework import serializers

from .models import Basket
from app.catalog.serializers import ImageSerializer, TagSerializer


class BasketSerializer(serializers.ModelSerializer):
    """
    Сериализатор корзины.
    """

    category = serializers.IntegerField(source="product.category_id")
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    freeDelivery = serializers.BooleanField(source="product.freeDelivery")
    images = ImageSerializer(source="product.images", many=True)
    tags = TagSerializer(source="product.tags", many=True)
    reviews = serializers.IntegerField(source="product.reviews")
    rating = serializers.DecimalField(
        source="product.rating",
        max_digits=2,
        decimal_places=1,
    )

    class Meta:
        model = Basket
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
