from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status

from .models import Payment
from app.orders.models import Order
from .serializers import PaymentSerializer


class PaymentAPIView(APIView):
    def post(self, request, id):
        order = get_object_or_404(Order.objects.filter(id=id))

        if hasattr(order, "payment"):
            return Response(
                ["payment already exists for this order"],
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Payment.objects.create(
            order=order,
            status="paid",
            transactionID=f"TX-{order.id}"
        )

        order.status = "paid"
        order.save()

        return Response(["Payment has been created"], status=status.HTTP_200_OK)
