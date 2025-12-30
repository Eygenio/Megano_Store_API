from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.basket.services import BasketService
from .models import Order, OrderItem, DeliverySettings
from .serializers import OrderSerializer


class OrderAPIView(APIView):
    def get(self, request):
        """
        Возвращает список активных заказов.
        """
        if not request.user.is_authenticated:
            return Response(status=401)

        orders = Order.objects.filter(user=request.user).prefetch_related(
            "products", "products__category", "products__images", "products__tags"
        )
        serializers = OrderSerializer(
            orders,
            many=True,
            context={"request": request}
        )
        return Response(serializers.data)

    def post(self, request):
        """
        Создание заказа, на основе корзины.
        """
        items = BasketService.get_items(request)

        if not items:
            return Response({"error": "Basket is empty"}, status=400)

        data = request.data if isinstance(request.data, dict) else {}

        if request.user.is_authenticated:
            data.setdefault("fullName", getattr(request.user, "fullname", ""))
            data.setdefault("email", getattr(request.user, "email", ""))
            data.setdefault("phone", getattr(request.user, "phone", ""))

        total_cost = 0
        for item in items:
            product = item["product"]
            count = item["count"]
            total_cost += product.price * count

        settings = DeliverySettings.objects.first()
        delivery_cost = 0
        delivery_type = data.get("deliveryType", "delivery")
        if delivery_type == "express":
            delivery_cost = settings.express_delivery_price
        else:
            if total_cost < settings.free_delivery_threshold:
                delivery_cost = settings.delivery_price

        total_cost += delivery_cost

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            fullName=data.get("fullName", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            deliveryType=data.get("deliveryType", ""),
            paymentType=data.get("paymentType", ""),
            totalCost=total_cost,
            status="accepted",
            city=data.get("city", ""),
            address=data.get("address", ""),
        )

        for item in items:
            product = item["product"]
            count = item["count"]

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                category=product.category,
                price=product.price * count,
                count=count,
                title=product.title,
                description=product.description,
                freeDelivery=product.freeDelivery,
                reviews=product.reviews,
                rating=product.rating,
            )

            order_item.images.set(product.images.all())
            order_item.tags.set(product.tags.all())

        BasketService.clear(request)

        serializer = OrderSerializer(order, context={"request": request})
        return Response({"orderId": serializer.data["id"]}, status=201)


class OrderIDAPIView(APIView):
    def get(self, request, id):
        """
        Возвращает заказ по ID.
        """
        if not request.user.is_authenticated:
            return Response(status=403)

        order = get_object_or_404(
            Order.objects.prefetch_related(
                "products", "products__images", "products__tags"
            ),
            id=id,
            user=request.user,
        )

        serializer = OrderSerializer(order, context={"request": request})
        return Response(serializer.data)

    def post(self, request, id):
        """
        Обновление статуса заказа по ID.
        """
        if not request.user.is_authenticated:
            return Response(status=403)

        order = get_object_or_404(Order, id=id, user=request.user)

        status = request.data.get("status")
        if status:
            order.status = status
            order.save()

        return Response({"orderId": order.id}, status=200)
