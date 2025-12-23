from django.urls import path

from .views import (
    CategoriesListAPIView,
    ProductPopularAPIView,
    ProductLimitedAPIView,
    ProductAPIView,
    ReviewAPIView,
    SalesAPIView,
    TagListAPIView,
    BannerListAPIView,
    CatalogAPIView,
)


app_name = "catalog"

urlpatterns = [
    path("api/categories/", CategoriesListAPIView.as_view(), name="categories"),
    path("api/catalog/", CatalogAPIView.as_view(), name="catalog"),
    path("api/products/popular/", ProductPopularAPIView.as_view(), name="products_popular"),
    path("api/products/limited/", ProductLimitedAPIView.as_view(), name="products_limited"),
    path("api/sales/", SalesAPIView.as_view(), name="sales"),
    path("api/banners/", BannerListAPIView.as_view(), name="banners"),
    path("api/tags/", TagListAPIView.as_view(), name="tags"),
    path("api/product/<int:id>/", ProductAPIView.as_view(), name="product"),
    path("api/product/<int:id>/review/", ReviewAPIView.as_view(), name="product_review"),
]
