from django.urls import path

from .views import OrderAPIView, OrderIDAPIView


app_name = "orders"

urlpatterns = [
    path("orders/", OrderAPIView.as_view(), name="orders"),
    path("order/<int:id>/", OrderIDAPIView.as_view(), name="order"),
]
