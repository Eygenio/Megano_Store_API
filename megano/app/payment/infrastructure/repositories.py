from app.orders.models import Order
from app.payment.constants import PAYMENT_STATUS_PAID
from app.payment.models import Payment


class PaymentRepository:
    def get_order_for_payment(self, order_id: int) -> Order:
        return Order.objects.get(id=order_id)

    def save_payment(self, payment: Payment) -> Payment:
        payment.save()
        return payment

    def create_payment(self, order, transaction_id: str):
        return Payment.objects.create(
            order=order, status=PAYMENT_STATUS_PAID, transactionId=transaction_id
        )
