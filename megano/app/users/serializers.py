from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

from app.core.serializers import ImageSerializer


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="fullname")
    avatar = ImageSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("fullName", "email", "phone", "avatar")


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "fullname", "phone")

    def create(self, validated_data):
        if "username" not in validated_data:
            validated_data["username"] = validated_data["email"]

        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        user = authenticate(
            username=data["username"],
            password=data["password"]
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
