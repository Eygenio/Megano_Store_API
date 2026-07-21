from decimal import Decimal
from typing import TYPE_CHECKING

from app.basket.domain.exceptions import EmptyBasketError, InsufficientStockError

if TYPE_CHECKING:
    from app.catalog.models import Product


class BasketDomainService:
    @staticmethod
    def calculate_item_price(product: Product, count: int) -> Decimal:
        if count <= 0:
            raise ValueError("Count must be positive")
        return product.price * count

    @staticmethod
    def calculate_total_price(items: list[dict]) -> Decimal:
        if not items:
            raise EmptyBasketError("Cannot calculate total for empty basket")

        total = Decimal("0.00")
        for item in items:
            product = item["product"]
            count = item["count"]
            total += product.price * count
        return total

    @staticmethod
    def validate_stock(product: Product, requested_count: int) -> None:
        if product.count < requested_count:
            raise InsufficientStockError(
                product_id=product.id,
                requested=requested_count,
                available=product.count,
            )

    @staticmethod
    def validate_removal_count(current_count: int, remove_count: int) -> int:
        if remove_count <= 0:
            raise ValueError("Remove count must be positive")

        new_count = max(0, current_count - remove_count)
        return new_count

    @staticmethod
    def can_merge_baskets(guest_items: list[dict], user_items: list[dict]) -> bool:
        if not guest_items:
            return False

        total_counts = {}
        for item in user_items:
            product = item["product"]
            total_counts[product.id] = total_counts.get(product.id, 0) + item["count"]

        for item in guest_items:
            product = item["product"]
            new_count = total_counts.get(product.id, 0) + item["count"]
            if new_count > product.count:
                return False
            total_counts[product.id] = new_count

        return True
