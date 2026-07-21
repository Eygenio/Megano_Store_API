from django.urls import path

from app.payment.interfaces.views import PaymentAPIView

app_name = "payment"

urlpatterns = [
    path("<int:id>/", PaymentAPIView.as_view(), name="payment"),
]
