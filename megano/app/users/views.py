from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer
from app.core.models import Image

class ProfileAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

        user = User.objects.get(id=request.data.get("id"))

        user = get_object_or_404(
            User.objects
            .filter(id=request.user.id)
            .select_related("avatar")
        )

        serializer = UserSerializer(user)
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

        return Response({"status": "password changed"})


class ProfileAvatarAPIView(APIView):
    def post(self, request):
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
