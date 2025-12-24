from django.urls import path

from .views import OrderAPIView, OrderIDAPIView


app_name = "orders"

urlpatterns = [
    path("api/orders/", OrderAPIView.as_view(), name="orders"),
    path("api/orders/<int:id>", OrderIDAPIView.as_view(), name="order"),
]