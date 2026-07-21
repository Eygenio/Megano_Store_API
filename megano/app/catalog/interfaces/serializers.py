from typing import Any

from app.catalog.models import Category, Product, Review, Sales, Specification, Tag
from app.core.serializers import ImageSerializer
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict


class SubCategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Category
        fields = ("id", "title", "image")


class CategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    def to_representation(self, instance) -> dict[str, Any]:
        ret = super().to_representation(instance)
        return ret


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date")


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ("name", "value")


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(source="category_id")
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
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


class ProductFullSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(source="category_id")
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    reviews = ReviewSerializer(source="review_list", many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        )


class SalesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="product.id", read_only=True)

    price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )
    title = serializers.CharField(source="product.title")
    images = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = ("id", "price", "salePrice", "dateFrom", "dateTo", "title", "images")

    def get_images(self, obj) -> ReturnDict:
        request = self.context.get("request")

        return ImageSerializer(
            obj.product.images.all(), many=True, context={"request": request}
        ).data
