import logging

from app.payment.application.factories import PaymentUseCaseFactory
from app.payment.interfaces.serializers import PaymentSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class PaymentAPIView(APIView):
    def post(self, request: Request, id: int) -> Response:
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        factory = PaymentUseCaseFactory()
        use_case = factory.process_payment()
        try:
            result = use_case.execute(order_id=id)
            logger.info(
                "Payment processed for order #%d, transaction_id=%s",
                id,
                result.transaction_id,
            )
            return Response(
                {"transactionId": result.transaction_id}, status=status.HTTP_200_OK
            )
        except ValueError as e:
            logger.warning("Payment failed for order #%d: %s", id, e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
