from dataclasses import dataclass

from app.orders.constants import ORDER_STATUS_PAID
from app.payment.constants import PAYMENT_STATUS_PAID
from app.payment.domain.services import PaymentDomainService
from app.payment.dto import PaymentResultDTO
from app.payment.infrastructure.repositories import PaymentRepository


@dataclass
class ProcessPaymentUseCase:
    domain_service: PaymentDomainService
    payment_repo: PaymentRepository

    def execute(self, order_id: int) -> PaymentResultDTO:
        order = self.payment_repo.get_order_for_payment(order_id)

        if not self.domain_service.can_process_payment(order):
            raise ValueError("Payment already exists for this order")

        transaction_id = self.domain_service.generate_transaction_id(order)
        self.payment_repo.create_payment(order, transaction_id)

        order.status = ORDER_STATUS_PAID
        order.save(update_fields=["status"])

        return PaymentResultDTO(
            transaction_id=transaction_id,
            status=PAYMENT_STATUS_PAID,
        )
