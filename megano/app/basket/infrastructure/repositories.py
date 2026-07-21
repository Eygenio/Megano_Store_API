from typing import Any

from django.db.models import QuerySet

from app.basket.constants import SESSION_KEY
from app.basket.models import Basket
from app.catalog.models import Product


class BasketRepository:
    def get_user_items(self, user: Any) -> QuerySet[Basket]:
        return (
            Basket.objects.filter(user=user)
            .select_related("product", "product__category")
            .prefetch_related("product__images", "product__tags")
        )

    def get_user_items_as_list(self, user: Any) -> list[dict]:
        items = self.get_user_items(user)
        return [{"product": item.product, "count": item.count} for item in items]

    @staticmethod
    def add_item(user: Any, product: Product, count: int) -> Basket:

        item, created = Basket.objects.get_or_create(
            user=user,
            product=product,
            defaults={
                "count": count,
                "price": product.price * count,
            },
        )
        if not created:
            item.count += count
            item.price = item.count * product.price
            item.save(update_fields=["count", "price"])

        return item

    @staticmethod
    def remove_item(user: Any, product_id: int, count: int) -> None:
        item = Basket.objects.get(user=user, product_id=product_id)

        if count >= item.count:
            item.delete()
        else:
            item.count -= count
            item.price = item.count * item.product.price
            item.save(update_fields=["count", "price"])

    @staticmethod
    def clear_basket(user: Any) -> None:
        Basket.objects.filter(user=user).delete()

    @staticmethod
    def get_item_count(user: Any) -> int:
        return Basket.objects.filter(user=user).count()


class SessionBasketRepository:
    SESSION_KEY: str = SESSION_KEY

    def __init__(self, session: Any) -> None:
        self.session = session

    def _get_basket_data(self) -> dict[str, dict]:
        basket = self.session.get(self.SESSION_KEY)
        if not isinstance(basket, dict):
            basket = {}
            self.session[self.SESSION_KEY] = basket
        return basket

    def get_items(self) -> dict[str, dict]:
        return self._get_basket_data()

    def get_product_ids(self) -> list[int]:
        basket = self._get_basket_data()
        return [int(pid) for pid in basket.keys()]

    def get_items_with_products(self) -> list[dict]:
        basket = self._get_basket_data()
        if not basket:
            return []

        products = (
            Product.objects.filter(id__in=basket.keys())
            .select_related("category")
            .prefetch_related("images", "tags")
        )

        return [
            {"product": product, "count": basket[str(product.id)]["count"]}
            for product in products
        ]

    def add_item(self, product_id: int, count: int) -> None:
        basket = self._get_basket_data()
        pid = str(product_id)

        if pid not in basket:
            basket[pid] = {"count": 0}

        basket[pid]["count"] += count
        self.session.modified = True

    def remove_item(self, product_id: int, count: int) -> None:
        basket = self._get_basket_data()
        pid = str(product_id)

        if pid not in basket:
            return

        if count >= basket[pid]["count"]:
            del basket[pid]
        else:
            basket[pid]["count"] -= count

        self.session.modified = True

    def clear_basket(self) -> None:
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def get_item_count(self) -> int:
        basket = self._get_basket_data()
        return len(basket)
