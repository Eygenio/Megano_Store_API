from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrderDTO:
    delivery_type: str = "delivery"
    payment_type: str = ""
    city: str = ""
    address: str = ""
    full_name: str = ""
    email: str = ""
    phone: str = ""


@dataclass(frozen=True)
class OrderResultDTO:
    order_id: int
    total_cost: str
    status: str
