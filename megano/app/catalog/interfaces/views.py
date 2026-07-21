import logging

from app.catalog.application.factories import CatalogUseCaseFactory
from app.catalog.domain.exceptions import ProductNotFoundError
from app.catalog.dto import (
    CatalogFiltersDTO,
    CatalogRequestDTO,
    CatalogSortingDTO,
    ReviewDataDTO,
)
from app.catalog.interfaces.serializers import (
    CategorySerializer,
    ProductFullSerializer,
    ProductSerializer,
    ReviewSerializer,
    SalesSerializer,
    TagSerializer,
)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class CategoriesListAPIView(APIView):
    def get(self, request: Request) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_get_categories()
        categories = use_case.execute()
        serializer = CategorySerializer(
            categories, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductPopularAPIView(APIView):
    def get(self, request: Request) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_get_popular_products()
        products = use_case.execute()
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductLimitedAPIView(APIView):
    def get(self, request: Request) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_get_limited_products()
        products = use_case.execute()
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductAPIView(APIView):
    def get(self, request: Request, id: int) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_get_product()
        try:
            product = use_case.execute(id)
        except ProductNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductFullSerializer(product, context={"request": request})
        return Response(serializer.data)


class ReviewAPIView(APIView):
    def post(self, request: Request, id: int) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_add_review()
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review_dto = ReviewDataDTO(**serializer.validated_data)
        try:
            review_data = use_case.execute(id, review_dto)
            logger.info("Review added for product #%d by %s", id, review_dto.author)
        except ProductNotFoundError as e:
            logger.warning("Review attempt for non-existent product #%d", id)
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(review_data, status=status.HTTP_201_CREATED)


class SalesAPIView(APIView):
    def get(self, request: Request) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_get_sales()
        page = int(request.GET.get("currentPage", 1))
        result = use_case.execute(page)
        serializer = SalesSerializer(
            result["items"], many=True, context={"request": request}
        )
        return Response(
            {
                "items": serializer.data,
                "currentPage": result["currentPage"],
                "lastPage": result["lastPage"],
            }
        )


class TagListAPIView(APIView):
    def get(self, request: Request) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_get_tags()
        tags = use_case.execute()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class BannerListAPIView(APIView):
    def get(self, request: Request) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_get_banners()
        products = use_case.execute()
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


class CatalogAPIView(APIView):
    def get(self, request: Request) -> Response:
        factory = CatalogUseCaseFactory()
        use_case = factory.create_get_catalog()

        filters_dto = CatalogFiltersDTO(
            name=request.GET.get("filter[name]"),
            min_price=request.GET.get("filter[minPrice]"),
            max_price=request.GET.get("filter[maxPrice]"),
            free_delivery=request.GET.get("filter[freeDelivery]"),
            available=request.GET.get("filter[available]"),
            tags=request.GET.getlist("tags[]"),
        )
        sorting_dto = CatalogSortingDTO(
            sort_field=request.GET.get("sort"),
            sort_type=request.GET.get("sortType"),
        )
        page = int(request.GET.get("currentPage", 1))
        request_dto = CatalogRequestDTO(
            filters=filters_dto,
            sorting=sorting_dto,
            page=page,
        )

        result = use_case.execute(request_dto)
        serializer = ProductSerializer(
            result["items"], many=True, context={"request": request}
        )
        return Response(
            {
                "items": serializer.data,
                "currentPage": result["currentPage"],
                "lastPage": result["lastPage"],
            }
        )
