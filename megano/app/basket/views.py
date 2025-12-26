from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.catalog.models import Product
from .models import Basket
from .utils import build_product_short


def get_session_basket(request):
    basket = request.session.get("basket")
    if not isinstance(basket, dict):
        basket = {}
        request.session["basket"] = basket

    return basket


class BasketAPIView(APIView):
    def get(self, request):
        result = []

        if request.user.is_authenticated:
            items = (
                Basket.objects
                .filter(user=request.user)
                .select_related("product", "product__category")
                .prefetch_related("product__images", "product__tags")
            )
            for item in items:
                result.append(build_product_short(item.product, item.count))
            return Response(result)

        basket = request.session.get("basket", {})
        products = Product.objects.filter(id__in=basket.keys()).select_related("category").prefetch_related("images", "tags")
        for product in products:
            count = basket[str(product.id)]["count"]
            result.append(build_product_short(product, count))

        return Response(result)

    def post(self, request):
        product_id = str(request.data.get("id"))
        count = int(request.data.get("count", 1))
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            item, created = Basket.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={
                    "count": count,
                    "price": product.price * count
                }
            )
            if not created:
                item.count += count
                item.price = item.count * product.price
                item.save()
            return Response(status=200)

        basket = request.session.setdefault("basket", {})
        basket.setdefault(product_id, {"count": 0})
        basket[product_id]["count"] += count
        request.session.modified = True
        return Response(status=200)

    def delete(self, request):
        product_id = str(request.data.get("id"))
        count = int(request.data.get("count", 0))

        if request.user.is_authenticated:
            item = get_object_or_404(
                Basket,
                product_id=product_id,
                user=request.user
            )
            if count >= item.count:
                item.delete()
            else:
                item.count -= count
                item.price = item.count * item.product.price
                item.save()

            return Response(status=200)

        basket = request.session.get("basket", {})
        if product_id not in basket:
            return Response(status=200)

        if count >= basket[product_id]["count"]:
            del basket[product_id]
        else:
            basket[product_id]["count"] -= count

        request.session.modified = True
        return Response(status=200)
