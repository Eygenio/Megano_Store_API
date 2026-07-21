class PaymentDomainService:
    @staticmethod
    def can_process_payment(order) -> bool:
        return not hasattr(order, "payment")

    @staticmethod
    def generate_transaction_id(order) -> str:
        return f"TX-{order.id}"
