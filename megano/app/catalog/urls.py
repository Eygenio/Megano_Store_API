from django.urls import path, include

from .views import CategoriesListAPIView


app_name = "catalog"

urlpatterns = [
    path("api/categories/", CategoriesListAPIView.as_view(), name="categories"),
    # path('catalog/', catalog),
    # path('products/popular/', products_popular),
    # path('products/limited/', products_limited),
    # path('sales/', sales),
    # path('banners/', banners),
    # path('tags/', tags),
    # path('product/{id}/', product_detail),
    # path('product/{id}/review/', product_review),
]