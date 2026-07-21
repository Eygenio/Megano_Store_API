from decimal import Decimal

import pytest
from app.catalog.models import Product
from app.orders.domain.services import OrderDomainService
from app.orders.models import DeliverySettings

pytestmark = pytest.mark.django_db


class TestOrderDomainService:
    def test_calculate_items_total(
        self,
        product: Product,
        second_product: Product,
    ) -> None:
        items = [
            {"product": product, "count": 2},
            {"product": second_product, "count": 1},
        ]
        total = OrderDomainService.calculate_items_total(items)
        expected = product.price * 2 + second_product.price * 1
        assert total == expected

    def test_calculate_items_total_empty_raises(self) -> None:
        with pytest.raises(ValueError):
            OrderDomainService.calculate_items_total([])

    def test_calculate_delivery_cost_express(
        self,
        delivery_settings: None,
    ) -> None:
        settings = DeliverySettings.objects.first()
        cost = OrderDomainService.calculate_delivery_cost(
            settings, "express", Decimal("100")  # type: ignore[attr-defined]
        )
        assert cost == settings.express_delivery_price

    def test_calculate_delivery_cost_free_threshold(
        self,
        delivery_settings: None,
    ) -> None:
        settings = DeliverySettings.objects.first()
        total = Decimal(settings.free_delivery_threshold)  # точно равно порогу
        cost = OrderDomainService.calculate_delivery_cost(settings, "standard", total)
        assert cost == Decimal("0.00")

    def test_calculate_delivery_cost_standard(
        self,
        delivery_settings: None,
    ) -> None:
        settings = DeliverySettings.objects.first()
        cost = OrderDomainService.calculate_delivery_cost(
            settings, "ordinary", Decimal("200")  # type: ignore[attr-defined]
        )
        assert cost == settings.delivery_price  # type: ignore[attr-defined]
