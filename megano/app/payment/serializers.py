from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    """
    Сериализатор для оплаты заказа.
    """

    number = serializers.CharField(max_length=20, allow_blank=True)
    name = serializers.CharField(max_length=255, allow_blank=True)
    month = serializers.CharField(max_length=2, allow_blank=True)
    year = serializers.CharField(max_length=4, allow_blank=True)
    code = serializers.CharField(max_length=4, allow_blank=True)
