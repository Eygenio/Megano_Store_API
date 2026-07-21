class OrderDomainError(Exception):
    pass


class EmptyBasketError(OrderDomainError):
    pass
