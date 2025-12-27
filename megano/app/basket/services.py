from django.shortcuts import get_object_or_404

from app.catalog.models import Product
from .models import Basket


class BasketService:
    SESSION_KEY = "basket"

    @classmethod
    def _get_session_basket(cls, request) -> dict:
        basket = request.session.get(cls.SESSION_KEY)
        if not isinstance(basket, dict):
            basket = {}
            request.session[cls.SESSION_KEY] = basket
        return basket

    @classmethod
    def get_items(cls, request):

        if request.user.is_authenticated:
            items = (
                Basket.objects
                .filter(user=request.user)
                .select_related("product", "product__category")
                .prefetch_related("product__images", "product__tags")
            )
            return [
                {"product": item.product, "count": item.count}
                for item in items
            ]

        session_basket = cls._get_session_basket(request)
        if not session_basket:
            return []

        products = (
            Product.objects
            .filter(id__in=session_basket.keys())
            .select_related("category")
            .prefetch_related("images", "tags")
        )

        return [
            {
                "product": product,
                "count": session_basket[str(product.id)]["count"]
            }
            for product in products
        ]

    @classmethod
    def add(cls, request, product_id, count=1):
        count = int(count)
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            item, created = Basket.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={
                    "count": count,
                    "price": product.price * count,
                }
            )
            if not created:
                item.count += count
                item.price = item.count * product.price
                item.save()
            return

        basket = cls._get_session_basket(request)
        basket.setdefault(str(product_id), {"count": 0})
        basket[str(product_id)]["count"] += count
        request.session.modified = True

    @classmethod
    def remove(cls, request, product_id, count=1):
        count = int(count)

        if request.user.is_authenticated:
            item = get_object_or_404(
                Basket,
                user=request.user,
                product_id=product_id
            )
            if count >= item.count:
                item.delete()
            else:
                item.count -= count
                item.price = item.count * item.product.price
                item.save()
            return

        basket = cls._get_session_basket(request)
        key = str(product_id)

        if key not in basket:
            return

        if count >= basket[key]["count"]:
            del basket[key]
        else:
            basket[key]["count"] -= count

        request.session.modified = True

    @classmethod
    def clear(cls, request):
        if request.user.is_authenticated:
            Basket.objects.filter(user=request.user).delete()
        else:
            request.session[cls.SESSION_KEY] = {}
            request.session.modified = True
