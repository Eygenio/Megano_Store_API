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
    path("categories/", CategoriesListAPIView.as_view(), name="categories"),
    path("catalog/", CatalogAPIView.as_view(), name="catalog"),
    path("products/popular/", ProductPopularAPIView.as_view(), name="products_popular"),
    path("products/limited/", ProductLimitedAPIView.as_view(), name="products_limited"),
    path("sales/", SalesAPIView.as_view(), name="sales"),
    path("banners/", BannerListAPIView.as_view(), name="banners"),
    path("tags/", TagListAPIView.as_view(), name="tags"),
    path("product/<int:id>/", ProductAPIView.as_view(), name="product"),
    path("product/<int:id>/reviews/", ReviewAPIView.as_view(), name="product_review"),
]
