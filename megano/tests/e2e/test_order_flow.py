import json

import pytest
from app.catalog.models import Product
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestOrderFlow:
    def test_full_order_cycle(
        self,
        authenticated_client: APIClient,
        product: Product,
        second_product: Product,
        basket_url: str,
        orders_url: str,
        payment_url: str,
        delivery_settings: None,
        payment_payload: dict,
        order_payload: dict,
    ) -> None:
        authenticated_client.post(
            basket_url,
            json.dumps({"id": product.id, "count": 2}),
            content_type="text/plain",
        )
        authenticated_client.post(
            basket_url,
            json.dumps({"id": second_product.id, "count": 1}),
            content_type="text/plain",
        )
        response = authenticated_client.post(orders_url, order_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        order_id = response.data["orderId"]

        response = authenticated_client.post(
            f"{payment_url}{order_id}/", payment_payload, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

        response = authenticated_client.get(f"/api/order/{order_id}/")
        assert response.data["status"] == "paid"
