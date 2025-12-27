from rest_framework.views import APIView
from rest_framework.response import Response

from .services import BasketService
from .utils import build_product_short


class BasketAPIView(APIView):
    def get(self, request):
        items = BasketService.get_items(request)
        return Response([
            build_product_short(item["product"], item["count"])
            for item in items
        ])

    def post(self, request):
        BasketService.add(
            request,
            product_id=request.data["id"],
            count=request.data.get("count", 1),
        )
        return Response(status=200)

    def delete(self, request):
        BasketService.remove(
            request,
            product_id=request.data["id"],
            count=request.data.get("count", 1),
        )
        return Response(status=200)
