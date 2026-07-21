import pytest
from app.basket.domain.exceptions import EmptyBasketError, InsufficientStockError
from app.basket.domain.services import BasketDomainService
from app.catalog.models import Product

pytestmark = pytest.mark.django_db


class TestBasketDomainService:
    def test_calculate_item_price(
        self,
        product: Product,
    ) -> None:
        count = 3
        expected = product.price * count
        assert BasketDomainService.calculate_item_price(product, count) == expected

    def test_calculate_item_price_zero_count_raises(
        self,
        product: Product,
    ) -> None:
        service = BasketDomainService()
        with pytest.raises(ValueError, match="positive"):
            service.calculate_item_price(product, 0)

    def test_validate_stock_sufficient(
        self,
        product: Product,
    ) -> None:
        BasketDomainService.validate_stock(product, product.count - 1)

    def test_validate_stock_insufficient(
        self,
        product: Product,
    ) -> None:
        with pytest.raises(InsufficientStockError):
            BasketDomainService.validate_stock(product, product.count + 1)

    def test_calculate_total_price_empty_raises(self) -> None:
        with pytest.raises(EmptyBasketError):
            BasketDomainService.calculate_total_price([])

    def test_calculate_total_price(
        self,
        product: Product,
    ) -> None:
        items = [{"product": product, "count": 2}, {"product": product, "count": 3}]
        total = product.price * 2 + product.price * 3
        assert BasketDomainService.calculate_total_price(items) == total

    def test_validate_removal_count(self) -> None:
        assert BasketDomainService.validate_removal_count(5, 2) == 3
        assert BasketDomainService.validate_removal_count(2, 5) == 0

    def test_can_merge_baskets_true(
        self,
        product: Product,
        second_product: Product,
    ) -> None:
        guest = [{"product": product, "count": 1}]
        user_basket = [{"product": second_product, "count": 1}]
        assert BasketDomainService.can_merge_baskets(guest, user_basket) is True

    def test_can_merge_baskets_false_exceed_stock(
        self,
        product: Product,
    ) -> None:
        guest = [{"product": product, "count": product.count + 1}]
        assert BasketDomainService.can_merge_baskets(guest, []) is False
