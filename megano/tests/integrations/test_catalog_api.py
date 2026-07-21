import pytest
from app.catalog.models import Category, Product, Sales, Tag
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestCatalogAPI:
    def test_list_catalog(
        self,
        api_client: APIClient,
        catalog_url: str,
        product: Product,
    ) -> None:
        response = api_client.get(catalog_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["items"]) == 1

    def test_filter_by_name(
        self,
        api_client: APIClient,
        catalog_url: str,
        product: Product,
    ) -> None:
        response = api_client.get(f"{catalog_url}?filter[name]={product.title}")
        assert response.data["items"][0]["title"] == product.title

    def test_product_detail(
        self,
        api_client: APIClient,
        product: Product,
    ) -> None:
        url = f"/api/product/{product.id}/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == product.id

    def test_product_not_found(
        self,
        api_client: APIClient,
    ) -> None:
        response = api_client.get("/api/product/999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_categories_list(
        self,
        api_client: APIClient,
        categories_url: str,
        category: Category,
    ) -> None:
        response = api_client.get(categories_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_popular_products(
        self,
        api_client: APIClient,
        product: Product,
    ) -> None:
        response = api_client.get("/api/products/popular/")
        assert response.status_code == status.HTTP_200_OK

    def test_limited_products(
        self,
        api_client: APIClient,
        limited_product: Product,
    ) -> None:
        response = api_client.get("/api/products/limited/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_sales_list(
        self,
        api_client: APIClient,
        sale_product: Sales,
    ) -> None:
        response = api_client.get("/api/sales/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["items"]) == 1

    def test_tags_list(
        self,
        api_client: APIClient,
        tag: Tag,
    ) -> None:
        response = api_client.get("/api/tags/")
        assert response.status_code == status.HTTP_200_OK

    def test_banners(
        self,
        api_client: APIClient,
        product: Product,
    ) -> None:
        response = api_client.get("/api/banners/")
        assert response.status_code == status.HTTP_200_OK
