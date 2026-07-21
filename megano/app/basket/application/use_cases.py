from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from django.db import transaction

from app.basket.domain.services import BasketDomainService
from app.basket.dto import AddToBasketDTO, RemoveFromBasketDTO
from app.basket.infrastructure.repositories import (
    BasketRepository,
    SessionBasketRepository,
)
from app.catalog.models import Product


@dataclass
class AddToBasketUseCase:
    domain_service: BasketDomainService
    user_repo: BasketRepository
    session_repo: SessionBasketRepository

    def execute(
        self,
        user: Any,
        dto: AddToBasketDTO,
    ) -> None:
        if dto.count <= 0:
            raise ValueError("Count must be positive")

        product = Product.objects.select_for_update().get(id=dto.product_id)

        self.domain_service.validate_stock(product, dto.count)

        if user and user.is_authenticated:
            self.user_repo.add_item(user, product, dto.count)
        else:
            self.session_repo.add_item(dto.product_id, dto.count)


@dataclass
class RemoveFromBasketUseCase:
    domain_service: BasketDomainService
    user_repo: BasketRepository
    session_repo: SessionBasketRepository

    def execute(
        self,
        user: Any,
        dto: RemoveFromBasketDTO,
    ) -> None:
        if dto.count <= 0:
            raise ValueError("Count must be positive")

        if user and user.is_authenticated:
            self.user_repo.remove_item(user, dto.product_id, dto.count)
        else:
            self.session_repo.remove_item(dto.product_id, dto.count)


@dataclass
class GetBasketUseCase:
    user_repo: BasketRepository
    session_repo: SessionBasketRepository

    def execute(self, user: Any) -> list[dict]:
        if user and user.is_authenticated:
            return self.user_repo.get_user_items_as_list(user)
        else:
            return self.session_repo.get_items_with_products()


@dataclass
class ClearBasketUseCase:
    user_repo: BasketRepository
    session_repo: SessionBasketRepository

    def execute(self, user: Any) -> None:
        if user and user.is_authenticated:
            self.user_repo.clear_basket(user)
        else:
            self.session_repo.clear_basket()


@dataclass
class MergeBasketsUseCase:
    domain_service: BasketDomainService
    user_repo: BasketRepository
    session_repo: SessionBasketRepository

    @transaction.atomic
    def execute(self, user: Any) -> None:
        guest_items = self.session_repo.get_items_with_products()

        if not guest_items:
            return

        user_items = self.user_repo.get_user_items_as_list(user)
        if not self.domain_service.can_merge_baskets(guest_items, user_items):
            raise ValueError("Cannot merge baskets: insufficient stock")

        for item in guest_items:
            self.user_repo.add_item(user, item["product"], item["count"])

        self.session_repo.clear_basket()


@dataclass
class CalculateBasketTotalUseCase:
    domain_service: BasketDomainService

    def execute(self, items: list[dict]) -> Decimal:
        return self.domain_service.calculate_total_price(items)
