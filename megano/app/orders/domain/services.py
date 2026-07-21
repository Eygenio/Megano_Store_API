from decimal import Decimal
from typing import TYPE_CHECKING

from app.orders.constants import DELIVERY_TYPE_EXPRESS

if TYPE_CHECKING:
    from app.orders.models import DeliverySettings


class OrderDomainService:

    @staticmethod
    def calculate_items_total(items: list[dict]) -> Decimal:
        if not items:
            raise ValueError("Items list cannot be empty")
        return sum(item["product"].price * item["count"] for item in items)

    @staticmethod
    def calculate_delivery_cost(
        settings: "DeliverySettings", delivery_type: str, items_total: Decimal
    ) -> Decimal:
        if delivery_type == DELIVERY_TYPE_EXPRESS:
            return settings.express_delivery_price
        if items_total >= settings.free_delivery_threshold:
            return Decimal("0.00")
        return settings.delivery_price
