import json
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import BasketService
from .utils import build_product_short


class BasketAPIView(APIView):
    parser_classes = (JSONParser, FormParser)

    def get(self, request):
        """
        Возвращает все товары ноходящиеся в корзине.
        """
        items = BasketService.get_items(request)
        return Response(
            [
                build_product_short(item["product"], item["count"], request)
                for item in items
            ]
        )

    def post(self, request):
        """
        Добавление товара в корзину.
        """
        data = self._get_data(request)
        BasketService.add(
            request,
            product_id=data["id"],
            count=data.get("count", 1),
        )
        return Response(status=200)

    def delete(self, request):
        """
        Удаление товара из корзины.
        """
        data = self._get_data(request)
        BasketService.remove(
            request,
            product_id=data["id"],
            count=data.get("count", 1),
        )
        return Response(status=200)

    def _get_data(self, request):
        """
        Универсальный парссер данных
        Поддерживает JSON + text/plain.
        """
        if request.content_type.startswith("text/plain"):
            return json.loads(request.body.decode("utf-8"))
        return request.data
