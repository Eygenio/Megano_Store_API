from django.urls import path

from .views import BasketAPIView


app_name ="basket"

urlpatterns = [
    path("api/basket/", BasketAPIView.as_view(), name="basket"),
]
