from django.test import TestCase
from app.users.models import User
from app.catalog.models import Category, Product
from app.basket.services import BasketService
from app.orders.models import Order
from app.orders.models import DeliverySettings


class OrderAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")

        self.category = Category.objects.create(title="Phones")
        self.product = Product.objects.create(
            category=self.category, title="Phone", price=100, count=5
        )

        DeliverySettings.objects.create(
            delivery_price=200, express_delivery_price=500, free_delivery_threshold=1000
        )

    def test_create_order_with_delivery(self):
        self.client.login(username="test", password="12345")

        request = self.client.get("/").wsgi_request
        request.user = self.user

        BasketService.add(request, self.product.id, 1)

        response = self.client.post(
            "/api/orders/",
            {"deliveryType": "standard"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
