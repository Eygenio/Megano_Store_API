from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from app.orders.models import Order
from .serializers import PaymentSerializer
from .models import Payment


class PaymentAPIView(APIView):
    def post(self, request, id):
        """
        Оплата заказа по ID.
        """
        order = get_object_or_404(Order, id=id)

        if hasattr(order, "payment"):
            return Response(
                ["payment already exists for this order"],
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Payment.objects.create(
            order=order, status="paid", transactionId=f"TX-{order.id}"
        )

        order.status = "paid"
        order.save()

        return Response(["Payment has been created"], status=status.HTTP_200_OK)
