import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth import login, logout, update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

from .serializers import UserSerializer, SignUpSerializer, SignInSerializer
from .utils import FormJSONParser
from app.basket.services import BasketService
from app.core.models import Image


class ProfileAPIView(APIView):
    def get(self, request):
        """
        Возращает данные пользователя.
        """
        if not request.user.is_authenticated:
            return Response(status=401)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        """
        Обновляет информацию пользоватееля.
        """
        user = request.user
        user.fullname = request.data.get("fullName", user.fullname)
        user.email = request.data.get("email", user.email)
        user.phone = request.data.get("phone", user.phone)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    def post(self, request):
        """
        Обновляет пароль пользователя.
        """
        if not request.user.is_authenticated:
            return Response(status=401)

        # password = request.data.get("password")
        password = (
            request.data
            if isinstance(request.data, str)
            else request.data.get("password")
        )

        if not password:
            return Response({"error": "Password required"}, status=400)

        request.user.set_password(password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        return Response({"status": "password changed"})


class ProfileAvatarAPIView(APIView):
    """
    Обновляет аватар польззователя.
    """

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

        avatar = request.FILES.get("avatar")
        if not avatar:
            return Response({"error": "NNo avatar"}, status=400)

        filename = default_storage.save(f"avatars/{uuid.uuid4()}_{avatar.name}", avatar)

        image = Image.objects.create(
            src=f"{settings.MEDIA_URL}{filename}",
            alt=f"{settings.MEDIA_URL}{filename}",
        )

        request.user.avatar = image
        request.user.save(update_fields=["avatar"])

        return Response({"src": image.src, "alt": image.alt})


class SignUpAPIView(APIView):
    parser_classes = (FormJSONParser, JSONParser)

    def post(self, request):
        """
        Регистрация пользователя.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class SignInAPIView(APIView):
    parser_classes = (FormJSONParser, JSONParser)

    def post(self, request):
        """
        Вход пользователя.
        """
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        guest_items = BasketService.get_items(request)

        login(request, user)

        for item in guest_items:
            BasketService.add(
                request,
                product_id=item["product"].id,
                count=item["count"]
            )

        BasketService.clear(request)

        return Response(status=status.HTTP_200_OK)


class SignOutAPIView(APIView):
    def post(self, request):
        """
        Выход пользователя.
        """
        logout(request)
        return Response(status=status.HTTP_200_OK)
