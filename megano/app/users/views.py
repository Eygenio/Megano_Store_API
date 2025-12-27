from django.contrib.auth import login, logout, update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, SignUpSerializer, SignInSerializer
from app.basket.services import BasketService
from app.core.models import Image
from app.catalog.models import Product
from app.basket.models import Basket

class ProfileAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        user.fullname = request.data.get("fullName", user.fullname)
        user.email = request.data.get("email", user.email)
        user.phone = request.data.get("phone", user.phone)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

        password = request.data.get("password")
        if not password:
            return Response({"error": "Password required"}, status=400)

        request.user.set_password(password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        return Response({"status": "password changed"})


class ProfileAvatarAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

        user = request.user

        image = Image.objects.create(
            src=request.data.get("src"),
            alt=request.data.get("alt"),
        )

        user.avatar = image
        user.save()

        return Response({
            "src": image.src,
            "alt": image.alt
        })


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class SignInAPIView(APIView):
    def post(self, request):
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
        logout(request)
        return Response(status=status.HTTP_200_OK)
