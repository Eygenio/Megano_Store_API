from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.basket.models import Basket
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderProductSerializer
from .utils import get_basket_items


class OrderAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

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
        items = get_basket_items(request)

        if not items:
            return Response(["Basket is empty"], status=400)

        total_cost = 0
        for item in items:
            if hasattr(item, "product"):
                total_cost += item.price
            else:
                total_cost += item.price * item.count_in_basket

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            fullName=request.data.get("fullName", getattr(request.user, "fullname", "")),
            email=request.data.get("email", getattr(request.user, "email", "")),
            phone=request.data.get("phone", getattr(request.user, "phone", "")),
            deliveryType=request.data.get("deliveryType"),
            paymentType=request.data.get("paymentType"),
            totalCost=total_cost,
            status="accepted",
            city=request.data.get("city"),
            address=request.data.get("address")
        )

        for item in items:
            product = item.product if hasattr(item, "product") else item
            count = item.count if hasattr(item, "count") else item.count_in_basket

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

        if request.user.is_authenticated:
            Basket.objects.filter(user=request.user).delete()
        else:
            request.session["basket"] = {}
            request.session.modified = True

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderIDAPIView(APIView):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=403)

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
        status  = request.data.get("status")
        if status:
            order.status = status
            order.save()

        return Response(["order updated"])
