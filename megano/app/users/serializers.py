from rest_framework import serializers
from .models import User

from app.core.serializers import ImageSerializer


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="fullname")
    avatar = ImageSerializer()

    class Meta:
        model = User
        fields = ("fullName", "email", "phone", "avatar")
