import json

import pytest
from app.users.models import User
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestAuthAPI:
    def test_sign_up(
        self,
        api_client: APIClient,
        sign_up_url: str,
        sign_up_payload: dict,
    ) -> None:
        response = api_client.post(
            sign_up_url,
            json.dumps(sign_up_payload),
            content_type="application/x-www-form-urlencoded",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_sign_in(
        self,
        api_client: APIClient,
        user: User,
        sign_in_url: str,
    ) -> None:
        data = {"username": user.username, "password": "testpass123"}
        response = api_client.post(
            sign_in_url,
            json.dumps(data),
            content_type="application/x-www-form-urlencoded",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_profile_requires_auth(
        self,
        api_client: APIClient,
    ) -> None:
        response = api_client.get("/api/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
