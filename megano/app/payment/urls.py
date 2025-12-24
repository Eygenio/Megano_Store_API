from django.urls import path

from .views import PaymentAPIView


app_name = "payment"

urlpatterns = [
    path("api/payment/<int:id>", PaymentAPIView.as_view(), name="payment"),
]
