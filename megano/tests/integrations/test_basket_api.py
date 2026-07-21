import json

import pytest
from app.catalog.models import Product
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestBasketAPI:
    def test_add_item_anonymous(
        self,
        api_client: APIClient,
        basket_url: str,
        product: Product,
    ) -> None:
        data = {"id": product.id, "count": 2}
        response = api_client.post(
            basket_url, json.dumps(data), content_type="text/plain"
        )
        assert response.status_code == status.HTTP_200_OK
        response = api_client.get(basket_url)
        assert response.data[0]["count"] == 2

    def test_add_item_authenticated(
        self,
        authenticated_client: APIClient,
        basket_url: str,
        product: Product,
    ) -> None:
        data = {"id": product.id, "count": 1}
        response = authenticated_client.post(
            basket_url, json.dumps(data), content_type="text/plain"
        )
        assert response.status_code == status.HTTP_200_OK
        response = authenticated_client.get(basket_url)
        assert len(response.data) == 1

    def test_remove_item(
        self,
        authenticated_client: APIClient,
        basket_url: str,
        product: Product,
    ) -> None:
        authenticated_client.post(
            basket_url,
            json.dumps({"id": product.id, "count": 3}),
            content_type="text/plain",
        )
        response = authenticated_client.delete(
            basket_url,
            json.dumps({"id": product.id, "count": 1}),
            content_type="text/plain",
        )
        assert response.status_code == status.HTTP_200_OK
        response = authenticated_client.get(basket_url)
        assert response.data[0]["count"] == 2

    def test_insufficient_stock_error(
        self,
        authenticated_client: APIClient,
        basket_url: str,
        product: Product,
    ) -> None:
        product.count = 1
        product.save()
        response = authenticated_client.post(
            basket_url,
            json.dumps({"id": product.id, "count": 5}),
            content_type="text/plain",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient stock" in str(response.data["error"])
