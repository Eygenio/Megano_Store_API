from typing import Any

from app.orders.models import DeliverySettings, Order, OrderItem


class OrderRepository:
    def get_user_orders(self, user: Any):
        return Order.objects.filter(user=user).prefetch_related(
            "products", "products__images", "products__tags", "products__category"
        )

    def get_order_by_id(self, order_id: int, user: Any | None = None) -> Order:
        qs = Order.objects.prefetch_related(
            "products", "products__images", "products__tags"
        )
        if user:
            return qs.get(id=order_id, user=user)
        return qs.get(id=order_id)

    def create_order(self, **fields) -> Order:
        return Order.objects.create(**fields)

    def update_order_status(self, order: Order, status: str) -> None:
        order.status = status
        order.save(update_fields=["status"])


class OrderItemRepository:
    def create_order_item(self, order: Order, item_data: dict) -> OrderItem:
        product = item_data["product"]
        count = item_data["count"]

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            category=product.category,
            price=product.price * count,
            count=count,
            title=product.title,
            description=product.description,
            freeDelivery=product.freeDelivery,
            reviews=product.reviews,
            rating=product.rating,
        )
        order_item.images.set(product.images.all())
        order_item.tags.set(product.tags.all())
        return order_item


class DeliverySettingsRepository:
    def get_settings(self) -> DeliverySettings:
        return DeliverySettings.objects.first()  # type: ignore[return-value]
