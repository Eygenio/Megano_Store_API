from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.basket.models import Basket
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderProductSerializer


class OrderAPIView(APIView):
    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related(
                "products",
                "products__category",
                "products__images",
                "products__tags"
            )
        )
        serializers = OrderSerializer(orders, many=True)
        return Response(serializers.data)

    def post(self, request):
        basket_items = Basket.objects.filter(user=request.user)

        if not basket_items.exists():
            return Response(["Basket is empty"], status=400)

        total_cost = sum(item.price for item in basket_items)

        order = Order.objects.create(
            user=request.user,
            fullName=request.user.full_name,
            email=request.user.email,
            phone=request.user.phone,
            deliveryType=request.data.get("deliveryType", "free"),
            paymentType=request.data.get("paymentType", "online"),
            totalCost=total_cost,
            status="accepted",
            city=request.data.get("city", ""),
            address=request.data.get("address", "")
        )

        for item in basket_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                category=item.product.category,
                pricce=item.price,
                count=item.count,
                title=item.product.title,
                description=item.product.description,
                freeDelivery=item.product.freeDelivery,
                reviews=item.product.reviews,
                rating=item.product.rating,
            )

            order_item.images.set(item.product.images.all())
            order_item.tags.set(item.product.tags.all())

        basket_items.delete()
        return Response(["Order created"])


class OrderIDAPIView(APIView):
    def get(self, request, id):
        order = get_object_or_404(
            Order,
            id=id,
            user=request.user
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request, id):
        order = get_object_or_404(
            Order,
            id=id,
            user=request.user
        )

        order.status = request.data.get("status", order.status)
        order.save()
        return Response(["order updated"])
