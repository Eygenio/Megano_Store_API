from rest_framework import serializers
from .models import Category, Tag, Review, Product, Specification, Sale

from app.core.serializers import ImageSerializer


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
            "rating"
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
            "rating"
        )


class SaleSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2
    )
    title = serializers.CharField(source="product.title")
    images = ImageSerializer(source="product.images", many=True)

    class Meta:
        model = Sale
        fields = (
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images"
        )
