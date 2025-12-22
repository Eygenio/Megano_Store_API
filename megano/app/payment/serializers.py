from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=255)
    month = serializers.CharField(max_length=2)
    year = serializers.CharField(max_length=4)
    code = serializers.CharField(max_length=4)
