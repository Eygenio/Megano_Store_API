from app.core.models import Image
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ("src", "alt")

    def get_src(self, obj) -> str | None:
        request = self.context.get("request")

        if not obj.src:
            return None

        src = obj.src
        if not src.startswith("/"):
            src = "/" + src

        if request:
            return request.build_absolute_uri(src)
        return src
