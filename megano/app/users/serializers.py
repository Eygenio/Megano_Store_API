from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

from app.core.serializers import ImageSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.
    Используется для выведения информации о пользователе.
    """

    fullName = serializers.CharField(source="fullname")
    avatar = ImageSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("fullName", "email", "phone", "avatar")


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сеериализатор для регистарции пользователя.
    """

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    fullname = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "fullname", "phone")

    def create(self, validated_data):
        """
        Создает пользователя.
        """
        password = validated_data.pop("password")
        if not validated_data.get("fullname"):
            validated_data["fullname"] = validated_data.get("username", "")

        if not validated_data.get("email"):
            validated_data["email"] = f'{validated_data["username"]}@example.com'

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SignInSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя.
    """

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Проверяет, валидность данных для входа.
        """
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
