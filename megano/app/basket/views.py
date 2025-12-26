from os import cpu_count

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.catalog.models import Product
from .models import Basket
from .serializers import BasketSerializer
from ..catalog.serializers import TagSerializer
from ..core.serializers import ImageSerializer


def get_session_basket(request):
    basket = request.session.get("basket")
    if not isinstance(basket, dict):
        basket = {}
        request.session["basket"] = basket

    return basket


class BasketAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            basket = (
                Basket.objects
                .filter(user=request.user)
                .select_related("product", "product__category")
                .prefetch_related("product__images", "product__tags")
            )
            serializer = BasketSerializer(basket)
            return Response(serializer.data)

        session_basket = get_session_basket(request)
        products = Product.objects.filter(id__in=session_basket.keys()).select_related("category").prefetch_related("images", "tags")
        result = []
        for product in products:
            count = session_basket[str(product.id)]["count"]
            result.append({
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
                "reviews":  product.reviews,
                "rating": product.rating,
            })
        return Response(result)

    def post(self, request):
        product_id = request.data.get("id")
        count = int(request.data.get("count", 1))

        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            basket_item, created = Basket.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={
                    "count": count,
                    "price": product.price * count
                }
            )
            if not created:
                basket_item.cont += count
                basket_item.price = basket_item.count * product.price
                basket_item.save()

            serializer = BasketSerializer(basket_item)
            return Response(serializer.data)

        basket = get_session_basket(request)
        if product_id in basket:
            basket[product_id]["count"] += count
        else:
            basket[product_id] = {"count": count}

        request.session.modified = True

        return Response(["product added"])

    def delete(self, request):
        basket_id = request.data.get("id")
        count = int(request.data.get("count", 0))

        if request.user_is_authenticated:
            basket_item = get_object_or_404(
                Basket,
                id=basket_id,
                user=request.user
            )
            if count >= basket_item.count:
                basket_item.delete()
            else:
                basket_item.count -= count
                basket_item.price = basket_item.count * basket_item.product.price
                basket_item.save()

            return Response(["Items deleted"])

        basket = get_session_basket(request)
        if basket_id not in basket:
            return Response(["Item not found"])

        if count >= basket[basket_id]["count"]:
            del basket[basket_id]
        else:
            basket[basket_id]["count"] -= count

        request.session.modified = True
        return Response(["Item deleted"])



