from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentRequestDTO:
    number: str
    name: str
    month: str
    year: str
    code: str


@dataclass(frozen=True)
class PaymentResultDTO:
    transaction_id: str
    status: str = "paid"
