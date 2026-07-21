import logging
import uuid

from django.conf import settings
from django.contrib.auth import login, logout, update_session_auth_hash
from django.core.files.storage import default_storage

from app.basket.application.factories import BasketUseCaseFactory
from app.basket.dto import AddToBasketDTO
from app.core.models import Image
from app.users.serializers import SignInSerializer, SignUpSerializer, UserSerializer
from app.users.utils import FormJSONParser
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class ProfileAPIView(APIView):
    def get(self, request: Request) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        user = request.user
        user.fullname = request.data.get("fullName", user.fullname)
        user.email = request.data.get("email", user.email)
        user.phone = request.data.get("phone", user.phone)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    def post(self, request: Request) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        password = (
            request.data
            if isinstance(request.data, str)
            else request.data.get("password")
        )

        if not password:
            return Response(
                {"error": "Password required"}, status=status.HTTP_400_BAD_REQUEST
            )

        request.user.set_password(password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        return Response({"status": "password changed"})


class ProfileAvatarAPIView(APIView):
    def post(self, request: Request) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        avatar = request.FILES.get("avatar")
        if not avatar:
            return Response({"error": "No avatar"}, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request: Request) -> Response:
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        logger.info("New user registered and signed in: %s", user)
        return Response(status=status.HTTP_200_OK)


class SignInAPIView(APIView):
    parser_classes = (FormJSONParser, JSONParser)

    def post(self, request: Request) -> Response:
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        logger.info("User %s attempting to sign in", user)

        factory = BasketUseCaseFactory(request)
        get_basket = factory.create_get_basket()
        guest_items = get_basket.execute(None)

        login(request, user)

        if guest_items:
            add_to_basket = factory.create_add_to_basket()
            for item in guest_items:
                dto = AddToBasketDTO(
                    product_id=item["product"].id,
                    count=item["count"],
                )
                add_to_basket.execute(
                    user=user,
                    dto=dto,
                )

        clear_basket = factory.create_clear_basket()
        clear_basket.execute(None)
        logger.info("User %s signed in successfully, guest basket merged", user)

        return Response(status=status.HTTP_200_OK)


class SignOutAPIView(APIView):
    def post(self, request: Request) -> Response:
        user = request.user
        logout(request)
        logger.info("User %s signed out", user)
        return Response(status=status.HTTP_200_OK)
