from typing import TYPE_CHECKING

from app.catalog.interfaces.serializers import TagSerializer
from app.core.serializers import ImageSerializer

if TYPE_CHECKING:
    from django.http import HttpRequest

    from app.catalog.models import Product


def build_product_short(
    product: Product,
    count: int,
    request: HttpRequest,
) -> dict:
    return {
        "id": product.id,
        "category": product.category_id,
        "price": product.price,
        "count": count,
        "date": None,
        "title": product.title,
        "description": product.description,
        "freeDelivery": product.freeDelivery,
        "images": ImageSerializer(
            product.images.all(), many=True, context={"request": request}
        ).data,
        "tags": TagSerializer(product.tags.all(), many=True).data,
        "reviews": product.reviews,
        "rating": product.rating,
    }
