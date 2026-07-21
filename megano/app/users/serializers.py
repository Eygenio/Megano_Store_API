from typing import Any

from django.contrib.auth import authenticate

from app.core.serializers import ImageSerializer
from app.users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="fullname")
    avatar = ImageSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("fullName", "email", "phone", "avatar")


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    fullname = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "fullname", "phone")

    def create(self, validated_data: dict[str, Any]) -> User:
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
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data) -> dict[str, Any]:
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
