from decimal import Decimal

import pytest
from app.catalog.domain.services import CatalogDomainService
from app.catalog.models import Product
from tests.conftest import fake

pytestmark = pytest.mark.django_db


class TestCatalogDomainService:
    def test_apply_filters_name(
        self,
        product: Product,
        second_product: Product,
    ) -> None:
        qs = Product.objects.all()
        filtered = CatalogDomainService.apply_filters(
            qs, {"name": second_product.title}
        )
        assert list(filtered) == [second_product]

    def test_apply_filters_price_range(
        self,
        product: Product,
        second_product: Product,
    ) -> None:
        qs = Product.objects.all()
        min_price = str(second_product.price - 1)
        max_price = str(second_product.price + 1)
        filtered = CatalogDomainService.apply_filters(
            qs, {"minPrice": min_price, "maxPrice": max_price}
        )
        assert second_product in filtered
        assert product not in filtered

    def test_apply_filters_free_delivery(
        self,
        product: Product,
        second_product: Product,
    ) -> None:
        qs = Product.objects.all()
        filtered = CatalogDomainService.apply_filters(qs, {"freeDelivery": "true"})
        for prod in filtered:
            assert prod.freeDelivery is True

    def test_apply_sorting(
        self,
        product: Product,
        second_product: Product,
    ) -> None:
        qs = Product.objects.all()
        sorted_qs = CatalogDomainService.apply_sorting(qs, "price", "inc")
        prices = [p.price for p in sorted_qs]
        assert prices == sorted(prices)

    def test_recalculate_rating(
        self,
        product: Product,
    ) -> None:
        product.review_list.create(
            author=fake.name(),
            email=fake.email(),
            rate=4,
        )
        product.review_list.create(
            author=fake.name(),
            email=fake.email(),
            rate=5,
        )
        CatalogDomainService.recalculate_rating(product)
        product.refresh_from_db()
        assert product.reviews == 2
        assert product.rating == Decimal("4.5")
