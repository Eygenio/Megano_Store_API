class BasketDomainError(Exception):
    pass


class InsufficientStockError(BasketDomainError):
    def __init__(self, product_id: int, requested: int, available: int) -> None:
        self.product_id = product_id
        self.requested = requested
        self.available = available
        super().__init__(
            f"Insufficient stock for product {product_id}. "
            f"Requested: {requested}, Available: {available}"
        )


class BasketItemNotFoundError(BasketDomainError):
    def __init__(self, product_id: int, user_id: int | None = None) -> None:
        self.product_id = product_id
        self.user_id = user_id
        user_info = "user %s", user_id if user_id else "anonymous session"
        super().__init__(f"Product {product_id} not found in basket for {user_info}.")


class EmptyBasketError(BasketDomainError):
    pass
