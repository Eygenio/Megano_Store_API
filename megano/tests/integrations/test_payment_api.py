import json

import pytest
from app.catalog.models import Product
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestPaymentAPI:
    def test_process_payment(
        self,
        authenticated_client: APIClient,
        product: Product,
        basket_url: str,
        orders_url: str,
        payment_url: str,
        delivery_settings: None,
        payment_payload: dict,
    ) -> None:
        authenticated_client.post(
            basket_url,
            json.dumps({"id": product.id, "count": 1}),
            content_type="text/plain",
        )
        order_resp = authenticated_client.post(
            orders_url, {"deliveryType": "standard"}, format="json"
        )
        order_id = order_resp.data["orderId"]

        response = authenticated_client.post(
            f"{payment_url}{order_id}/", payment_payload, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert "transactionId" in response.data

    def test_double_payment_fails(
        self,
        authenticated_client: APIClient,
        product: Product,
        basket_url: str,
        orders_url: str,
        payment_url: str,
        delivery_settings: None,
        payment_payload: dict,
    ) -> None:
        authenticated_client.post(
            basket_url,
            json.dumps({"id": product.id, "count": 1}),
            content_type="text/plain",
        )
        order_resp = authenticated_client.post(
            orders_url, {"deliveryType": "standard"}, format="json"
        )
        order_id = order_resp.data["orderId"]

        authenticated_client.post(
            f"{payment_url}{order_id}/", payment_payload, format="json"
        )
        response = authenticated_client.post(
            f"{payment_url}{order_id}/", payment_payload, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
