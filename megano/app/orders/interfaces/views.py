import logging

from app.orders.application.factories import OrderUseCaseFactory
from app.orders.domain.exceptions import EmptyBasketError
from app.orders.dto import CreateOrderDTO
from app.orders.interfaces.serializers import OrderSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class OrderAPIView(APIView):
    def get(self, request: Request) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        factory = OrderUseCaseFactory(request)
        use_case = factory.get_user_orders()
        orders = use_case.execute(request.user)
        serializer = OrderSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        factory = OrderUseCaseFactory(request)
        use_case = factory.create_order()

        order_dto = CreateOrderDTO(
            delivery_type=request.data.get("deliveryType", "delivery"),
            payment_type=request.data.get("paymentType", ""),
            city=request.data.get("city", ""),
            address=request.data.get("address", ""),
            full_name=request.data.get("fullName", ""),
            email=request.data.get("email", ""),
            phone=request.data.get("phone", ""),
        )

        try:
            result = use_case.execute(user=request.user, dto=order_dto)
            logger.info(
                "Order #%d created successfully for user=%s",
                result.order_id,
                request.user,
            )
            return Response(
                {"orderId": result.order_id}, status=status.HTTP_201_CREATED
            )
        except EmptyBasketError as e:
            logger.warning(
                "Attempt to create order with empty basket by user=%s", request.user
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderIDAPIView(APIView):
    def get(self, request: Request, id: int) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        factory = OrderUseCaseFactory(request)
        use_case = factory.get_order_by_id()
        order = use_case.execute(order_id=id, user=request.user)
        serializer = OrderSerializer(order, context={"request": request})
        return Response(serializer.data)

    def post(self, request: Request, id: int) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        status_value = request.data.get("status")
        if not status_value:
            return Response(
                {"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        factory = OrderUseCaseFactory(request)
        use_case = factory.update_order_status()
        order_id = use_case.execute(
            order_id=id, user=request.user, new_status=status_value
        )
        logger.info("Order #%d status updated to '%s'", order_id, status_value)
        return Response({"orderId": order_id}, status=status.HTTP_200_OK)
