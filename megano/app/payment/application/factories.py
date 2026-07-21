from app.payment.application.use_cases import ProcessPaymentUseCase
from app.payment.domain.services import PaymentDomainService
from app.payment.infrastructure.repositories import PaymentRepository


class PaymentUseCaseFactory:
    def __init__(self):
        self._domain_service = None
        self._payment_repo = None

    @property
    def domain_service(self) -> PaymentDomainService:
        if not self._domain_service:
            self._domain_service = PaymentDomainService()
        return self._domain_service

    @property
    def payment_repo(self) -> PaymentRepository:
        if not self._payment_repo:
            self._payment_repo = PaymentRepository()
        return self._payment_repo

    def process_payment(self) -> ProcessPaymentUseCase:
        return ProcessPaymentUseCase(
            domain_service=self.domain_service,
            payment_repo=self.payment_repo,
        )
