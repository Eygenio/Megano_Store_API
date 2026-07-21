from dataclasses import dataclass


@dataclass(frozen=True)
class AddToBasketDTO:
    product_id: int
    count: int = 1


@dataclass(frozen=True)
class RemoveFromBasketDTO:
    product_id: int
    count: int = 1
