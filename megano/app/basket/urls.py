from django.urls import path

from app.basket.interfaces.views import BasketAPIView

app_name = "basket"

urlpatterns = [
    path("", BasketAPIView.as_view(), name="basket"),
]
