from dataclasses import dataclass
from typing import Any

from django.db import transaction

from app.basket.application.factories import BasketUseCaseFactory
from app.orders.constants import ORDER_STATUS_ACCEPTED
from app.orders.domain.exceptions import EmptyBasketError
from app.orders.domain.services import OrderDomainService
from app.orders.dto import CreateOrderDTO, OrderResultDTO
from app.orders.infrastructure.repositories import (
    DeliverySettingsRepository,
    OrderItemRepository,
    OrderRepository,
)


@dataclass
class CreateOrderUseCase:
    domain_service: OrderDomainService
    order_repo: OrderRepository
    order_item_repo: OrderItemRepository
    delivery_settings_repo: DeliverySettingsRepository
    basket_factory: BasketUseCaseFactory

    @transaction.atomic
    def execute(self, user: Any, dto: CreateOrderDTO) -> OrderResultDTO:
        get_basket = self.basket_factory.create_get_basket()
        items = get_basket.execute(user)

        if not items:
            raise EmptyBasketError("Cannot create order with empty basket")

        full_name = dto.full_name
        email = dto.email
        phone = dto.phone
        if user and user.is_authenticated:
            full_name = full_name or getattr(user, "fullname", "")
            email = email or getattr(user, "email", "")
            phone = phone or getattr(user, "phone", "")

        items_total = self.domain_service.calculate_items_total(items)
        settings = self.delivery_settings_repo.get_settings()
        delivery_cost = self.domain_service.calculate_delivery_cost(
            settings, dto.delivery_type, items_total
        )
        total_cost = items_total + delivery_cost

        order = self.order_repo.create_order(
            user=user if user and user.is_authenticated else None,
            fullName=full_name,
            email=email,
            phone=phone,
            deliveryType=dto.delivery_type,
            paymentType=dto.payment_type,
            totalCost=total_cost,
            status=ORDER_STATUS_ACCEPTED,
            city=dto.city,
            address=dto.address,
        )

        for item in items:
            self.order_item_repo.create_order_item(order, item)

        clear_basket = self.basket_factory.create_clear_basket()
        clear_basket.execute(user)

        return OrderResultDTO(
            order_id=order.id,
            total_cost=str(total_cost),
            status=ORDER_STATUS_ACCEPTED,
        )


@dataclass
class GetUserOrdersUseCase:
    order_repo: OrderRepository

    def execute(self, user: Any) -> list:
        return self.order_repo.get_user_orders(user)


@dataclass
class GetOrderByIdUseCase:
    order_repo: OrderRepository

    def execute(self, order_id: int, user: Any) -> Any:
        return self.order_repo.get_order_by_id(order_id, user)


@dataclass
class UpdateOrderStatusUseCase:
    order_repo: OrderRepository

    def execute(self, order_id: int, user: Any, new_status: str) -> int:
        order = self.order_repo.get_order_by_id(order_id, user)
        self.order_repo.update_order_status(order, new_status)
        return order.id
