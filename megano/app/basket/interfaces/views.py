import json
import logging
from typing import Any

from app.basket.application.factories import BasketUseCaseFactory
from app.basket.domain.exceptions import (
    BasketItemNotFoundError,
    InsufficientStockError,
)
from app.basket.dto import AddToBasketDTO, RemoveFromBasketDTO
from app.basket.utils import build_product_short
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class BasketAPIView(APIView):
    parser_classes = (JSONParser, FormParser)

    def get(self, request: Request) -> Response:
        factory = BasketUseCaseFactory(request)
        get_basket = factory.create_get_basket()
        items = get_basket.execute(request.user)
        logger.info("Basket retrieved: user=%s, items=%d", request.user, len(items))

        return Response(
            [
                build_product_short(item["product"], item["count"], request)
                for item in items
            ]
        )

    def post(self, request: Request) -> Response:
        data = self._parse_data(request)
        dto = AddToBasketDTO(
            product_id=data["id"],
            count=data.get("count", 1),
        )
        logger.debug(
            "Add to basket request: user=%s, product_id=%d, count=%d",
            request.user,
            dto.product_id,
            dto.count,
        )

        try:
            factory = BasketUseCaseFactory(request)
            add_to_basket = factory.create_add_to_basket()
            add_to_basket.execute(
                user=request.user,
                dto=dto,
            )
            logger.info(
                "Item added to basket: user=%s, product_id=%d, count=%d",
                request.user,
                dto.product_id,
                dto.count,
            )
            return Response(status=status.HTTP_200_OK)
        except InsufficientStockError as e:
            logger.warning("Insufficient stock: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            logger.warning("Validation error adding to basket: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        data = self._parse_data(request)
        dto = RemoveFromBasketDTO(
            product_id=data["id"],
            count=data.get("count", 1),
        )
        logger.debug(
            "Remove from basket request: user=%s, product_id=%d, count=%d",
            request.user,
            dto.product_id,
            dto.count,
        )

        try:
            factory = BasketUseCaseFactory(request)
            remove_from_basket = factory.create_remove_from_basket()
            remove_from_basket.execute(
                user=request.user,
                dto=dto,
            )
            logger.info(
                "Item removed from basket: user=%s, product_id=%d, count=%d",
                request.user,
                dto.product_id,
                dto.count,
            )
            return Response(status=status.HTTP_200_OK)
        except BasketItemNotFoundError as e:
            logger.warning("Basket item not found: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

    @staticmethod
    def _parse_data(request: Request) -> dict[str, Any]:
        if request.content_type.startswith("text/plain"):
            return json.loads(request.body.decode("utf-8"))
        return request.data
