from django.urls import path

from .views import OrderAPIView, OrderIDAPIView


app_name = "orders"

urlpatterns = [
    path("", OrderAPIView.as_view(), name="orders"),
    path("<int:id>/", OrderIDAPIView.as_view(), name="order"),
]