from rest_framework.test import APITestCase
from app.catalog.models import Category, Product


class BasketAPITest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Test")
        self.product = Product.objects.create(
            category=self.category, price=100, count=5, title="Phone"
        )

    def test_add_to_basket(self):
        response = self.client.post(
            "/api/basket/", {"id": self.product.id, "count": 2}, format="json"
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/basket/")
        self.assertEqual(len(response.data), 1)
