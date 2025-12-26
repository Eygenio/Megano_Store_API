from app.catalog.models import Product
from app.core.serializers import ImageSerializer
from app.catalog.serializers import TagSerializer


def build_product_short(product, count):
    return {
        "id": product.id,
        "category": product.category_id,
        "price": product.price * count,
        "count": count,
        "date": None,
        "title": product.title,
        "description": product.description,
        "freeDelivery": product.freeDelivery,
        "images": ImageSerializer(product.images.all(), many=True).data,
        "tags": TagSerializer(product.tags.all(), many=True).data,
        "reviews": product.reviews,
        "rating": product.rating,
    }
