from rest_framework.test import APITestCase
from app.catalog.models import Category, Product


class CatalogAPITest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Electronics")
        Product.objects.create(
            category=self.category, price=1000, count=10, title="Chuwi Laptop"
        )

    def test_search(self):
        response = self.client.get("/api/catalog/?filter=chuwi")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["items"]) > 0)
