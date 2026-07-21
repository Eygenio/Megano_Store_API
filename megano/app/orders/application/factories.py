from app.basket.application.factories import BasketUseCaseFactory
from app.orders.application.use_cases import (
    CreateOrderUseCase,
    GetOrderByIdUseCase,
    GetUserOrdersUseCase,
    UpdateOrderStatusUseCase,
)
from app.orders.domain.services import OrderDomainService
from app.orders.infrastructure.repositories import (
    DeliverySettingsRepository,
    OrderItemRepository,
    OrderRepository,
)


class OrderUseCaseFactory:
    def __init__(self, request=None):
        self.request = request
        self._domain_service = None
        self._order_repo = None
        self._order_item_repo = None
        self._delivery_settings_repo = None
        self._basket_factory = None

    @property
    def domain_service(self) -> OrderDomainService:
        if not self._domain_service:
            self._domain_service = OrderDomainService()
        return self._domain_service

    @property
    def order_repo(self) -> OrderRepository:
        if not self._order_repo:
            self._order_repo = OrderRepository()
        return self._order_repo

    @property
    def order_item_repo(self) -> OrderItemRepository:
        if not self._order_item_repo:
            self._order_item_repo = OrderItemRepository()
        return self._order_item_repo

    @property
    def delivery_settings_repo(self) -> DeliverySettingsRepository:
        if not self._delivery_settings_repo:
            self._delivery_settings_repo = DeliverySettingsRepository()
        return self._delivery_settings_repo

    @property
    def basket_factory(self) -> BasketUseCaseFactory:
        if not self._basket_factory:
            self._basket_factory = BasketUseCaseFactory(self.request)
        return self._basket_factory

    def create_order(self) -> CreateOrderUseCase:
        return CreateOrderUseCase(
            domain_service=self.domain_service,
            order_repo=self.order_repo,
            order_item_repo=self.order_item_repo,
            delivery_settings_repo=self.delivery_settings_repo,
            basket_factory=self.basket_factory,
        )

    def get_user_orders(self) -> GetUserOrdersUseCase:
        return GetUserOrdersUseCase(order_repo=self.order_repo)

    def get_order_by_id(self) -> GetOrderByIdUseCase:
        return GetOrderByIdUseCase(order_repo=self.order_repo)

    def update_order_status(self) -> UpdateOrderStatusUseCase:
        return UpdateOrderStatusUseCase(order_repo=self.order_repo)
