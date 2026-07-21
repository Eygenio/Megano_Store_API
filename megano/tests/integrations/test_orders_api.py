import json

import pytest
from app.catalog.models import Product
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestOrdersAPI:
    def test_create_order_success(
        self,
        authenticated_client: APIClient,
        product: Product,
        basket_url: str,
        orders_url: str,
        delivery_settings: None,
        order_payload: dict,
    ) -> None:
        authenticated_client.post(
            basket_url,
            json.dumps({"id": product.id, "count": 2}),
            content_type="text/plain",
        )
        response = authenticated_client.post(orders_url, order_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "orderId" in response.data

    def test_create_order_empty_basket(
        self,
        authenticated_client: APIClient,
        orders_url: str,
        delivery_settings: None,
    ) -> None:
        response = authenticated_client.post(orders_url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cannot create order with empty basket" in str(response.data["error"])

    def test_list_orders(
        self,
        authenticated_client: APIClient,
        orders_url: str,
    ) -> None:
        response = authenticated_client.get(orders_url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_order_by_id(
        self,
        authenticated_client: APIClient,
        product: Product,
        basket_url: str,
        orders_url: str,
        delivery_settings: None,
    ) -> None:
        authenticated_client.post(
            basket_url,
            json.dumps({"id": product.id, "count": 1}),
            content_type="text/plain",
        )
        create_resp = authenticated_client.post(
            orders_url, {"deliveryType": "standard"}, format="json"
        )
        order_id = create_resp.data["orderId"]
        response = authenticated_client.get(f"/api/order/{order_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == order_id

    def test_update_order_status(
        self,
        authenticated_client: APIClient,
        product: Product,
        basket_url: str,
        orders_url: str,
        delivery_settings: None,
    ) -> None:
        authenticated_client.post(
            basket_url,
            json.dumps({"id": product.id, "count": 1}),
            content_type="text/plain",
        )
        create_resp = authenticated_client.post(
            orders_url, {"deliveryType": "standard"}, format="json"
        )
        order_id = create_resp.data["orderId"]
        response = authenticated_client.post(
            f"/api/order/{order_id}/", {"status": "in_delivery"}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        get_resp = authenticated_client.get(f"/api/order/{order_id}/")
        assert get_resp.data["status"] == "in_delivery"
