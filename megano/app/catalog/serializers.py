from rest_framework import serializers
from .models import Category, Tag, Review, Product, Specification, Sales

from app.core.serializers import ImageSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор подкатегории товара.
    Используется в сериализаторе категории товаров.
    """

    image = ImageSerializer()

    class Meta:
        model = Category
        fields = ("id", "title", "image")


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории товара.
    Используется для каталога товаров.
    """

    image = ImageSerializer()
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор 'тегов'.
    Используется для возврата спискка 'тегов'.
    """

    class Meta:
        model = Tag
        fields = ("id", "name")


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов на ттовары.
    Используется для добавленния отзыва к товару.
    """

    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date")


class SpecificationSerializer(serializers.ModelSerializer):
    """
    Сериализатор характеристик товара.
    Используется в ссериализаторе полной информации о товаре.
    """

    class Meta:
        model = Specification
        fields = ("name", "value")


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выведения информации
    о товаре.
    Используется для выведения популярного, лимитируемого,
    списка товаров, а также списка тоавров для каталога и баннера.
    """

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
    """
    Сериалазатор для выведения полной
    инфоормации о товаре.
    Используется для выведения информации по ID товара.
    """

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
    """
    Сериализатор товаров на скидке.
    Исппользуется для возврата списка товаров на скидке.
    """

    id = serializers.IntegerField(source="product.id", read_only=True)

    price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )
    title = serializers.CharField(source="product.title")
    images = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = (
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images"
        )

    def get_images(self, obj):
        """
        Добавляет только основную ссылку
        на изображение товара на скидке.
        """
        request = self.context.get("request")

        return ImageSerializer(
            obj.product.images.all(),
            many=True,
            context={"request": request}
        ).data
