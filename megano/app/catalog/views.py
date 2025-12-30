from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg

from app.core.pagination import paginate_queryset
from .models import Category, Product, Review, Sales, Tag
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductFullSerializer,
    ReviewSerializer,
    SalesSerializer,
    TagSerializer,
)


class CategoriesListAPIView(APIView):
    def get(self, request):
        """
        Возввращает меню каталога.
        """
        categories = (
            Category.objects.filter(parent__isnull=True)
            .select_related("image")
            .prefetch_related("subcategories__image")
            .order_by("title")
        )

        serializer = CategorySerializer(
            categories, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductPopularAPIView(APIView):
    def get(self, request):
        """
        Возвращает список "популярных" товаров.
        """
        products = (
            Product.objects.select_related("category")
            .prefetch_related("images", "tags")
            .order_by("sortIndex", "-purchases")[:8]
        )
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductLimitedAPIView(APIView):
    def get(self, request):
        """
        Воозвращает список "лимитируемых" товаров.
        """
        products = (
            Product.objects.filter(limited=True)
            .select_related("category")
            .prefetch_related("images", "tags")[:16]
        )
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductAPIView(APIView):
    def get(self, request, id):
        """
        Возвращает товар из каталога по ID.
        """
        product = get_object_or_404(
            Product.objects.select_related("category").prefetch_related(
                "images", "tags", "specifications", "review_list"
            ),
            id=id,
        )
        serializer = ProductFullSerializer(product, context={"request": request})
        return Response(serializer.data)


class ReviewAPIView(APIView):
    def post(self, request, id):
        """
        Добавление отзыва на товар по ID.
        """
        product = get_object_or_404(Product, id=id)

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Review.objects.create(product=product, **serializer.validated_data)

        stats = Review.objects.filter(product=product).aggregate(
            reviews_count=Count("id"), avg_rating=Avg("rate")
        )

        product.reviews = stats["reviews_count"]
        product.rating = round(stats["avg_rating"], 2)
        product.save(update_fields=["reviews", "rating"])

        return Response(serializer.data, status=201)


class SalesAPIView(APIView):
    def get(self, request):
        """
        Возвращает список товаров со скидкой.
        Используется пагинация.
        """
        sales = Sales.objects.select_related("product")

        pagination = paginate_queryset(sales, request, per_page=8)
        serializer = SalesSerializer(
            pagination["items"], many=True, context={"request": request}
        )

        return Response(
            {
                "items": serializer.data,
                "currentPage": pagination["currentPage"],
                "lastPage": pagination["lastPage"],
            }
        )


class TagListAPIView(APIView):
    def get(self, request):
        """
        Возвращает список "тегов".
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class BannerListAPIView(APIView):
    def get(self, request):
        """
        Возвращает список товаров для баннера.
        """
        products = (
            Product.objects.filter(freeDelivery=True)
            .select_related("category")
            .prefetch_related("images", "tags")
        )
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


class CatalogAPIView(APIView):
    def get(self, request):
        """
        Возвращает список товаров из каталога.
        Используется фильтрация, сортировка и пагинация.
        """
        products = (
            Product.objects
            # .filter()
            .select_related("category").prefetch_related("images", "tags")
        )

        search = request.GET.get("filter")
        if search:
            products = products.filter(title__icontains=search)

        name = request.GET.get("filter[name]")
        if name:
            products = products.filter(title__icontains=name)

        min_price = request.GET.get("filter[minPrice]")
        if min_price:
            products = products.filter(price__gte=min_price)

        max_price = request.GET.get("filter[maxPrice]")
        if max_price:
            products = products.filter(price__lte=max_price)

        free_delivery = request.GET.get("filter[freeDelivery]")
        if free_delivery == "true":
            products = products.filter(freeDelivery=True)

        available = request.GET.get("filter[available]")
        if available == "true":
            products = products.filter(count__gt=0)

        tags = request.GET.getlist("tags[]")
        if tags:
            products = products.filter(tags__id__in=tags).distinct()

        sort_field = request.GET.get("sort")
        sort_type = request.GET.get("sortType")
        if sort_field:
            if sort_type == "inc":
                sort_field = f"-{sort_field}"
            products = products.order_by(sort_field)

        pagination = paginate_queryset(products, request, per_page=8)
        serializer = ProductSerializer(
            pagination["items"], many=True, context={"request": request}
        )

        return Response(
            {
                "items": serializer.data,
                "currentPage": pagination["currentPage"],
                "lastPage": pagination["lastPage"],
            }
        )
