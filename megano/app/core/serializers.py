from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображения.
    Используется для товаров и аватара пользователя.
    """

    src = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ("src", "alt")

    def get_src(self, obj):
        request = self.context.get("request")

        src = obj.src
        if not src.startswith("/"):
            src = "/" + src

        if request:
            return request.build_absolute_uri(src)
        return src
