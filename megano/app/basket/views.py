from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.catalog.models import Product
from .models import Basket
from .serializers import BasketSerializer


class BasketAPIView(APIView):
    def get(self, request):
        basket = (
            Basket.objects
            .filter(user=request.user)
            .select_related("product", "product__category")
            .prefetch_related("product__images", "product__tags")
        )
        serializer = BasketSerializer(basket)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("id")
        count = int(request.data.get("count", 1))

        product = get_object_or_404(Product, id=product_id)

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

    def delete(self, request):
        basket_id = request.data.get("id")
        count = int(request.data.get("count", 0))

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
