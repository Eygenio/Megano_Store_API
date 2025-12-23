from django.template.defaultfilters import title
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.core.pagination import paginate_queryset
from .models import Category, Product, Review, Sales, Tag
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductFullSerializer,
    ReviewSerializer,
    SalesSerializer,
    TagSerializer
)

class CategoriesListAPIView(APIView):
    def get(self, request):
        categories = (
            Category.objects
            .filter(parent__isnull=True)
            .select_related("image")
            .prefetch_related("subcategories__image")
        )

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductPopularAPIView(APIView):
    def get(self, request):
        products = (
            Product.objects
            .select_related("category")
            .prefetch_related("images", "tags")
            .order_by("sortIndex", "-purchases")[:8]
        )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductLimitedAPIView(APIView):
    def get(self, request):
        products = (
            Product.objects
            .filter(limited=True)
            .select_related("category")
            .prefetch_related("images", "tags")[:16]
        )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductAPIView(APIView):
    def get(self, request, id):
        product = get_object_or_404(
            Product.objects
            .select_related("category")
            .prefetch_related(
                "images",
                "tags",
                "specifications",
                "reviews"
            ),
            id=id
        )
        serializer = ProductFullSerializer(product)
        return Response(serializer.data)


class ReviewAPIView(APIView):
    def post(self, request, id):
        product = get_object_or_404(Product, id=id)

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Review.objects.create(
            product=product,
            **serializer.validated_data
        )
        return Response(serializer.data, status=201)


class SalesAPIView(APIView):
    def get(self, request):
        sales = Sales.objects.select_related("product")

        pagination = paginate_queryset(sales, request, per_page=8)
        serializer = SalesSerializer(pagination["items"], many=True)

        return Response({
            "items": serializer.data,
            "currentPage": pagination["currentPage"],
            "lastPage": pagination["lastPage"],
        })


class TagListAPIView(APIView):
    def get(self,request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class BannerListAPIView(APIView):
    def get(self, request):
        products = (Product.objects
                    .filter(freeDelivery=True)
                    .select_related("category")
                    .prefetch_related("images","tags")
                    )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class CatalogAPIView(APIView):
    def get(self, request):
        products = (Product.objects
                    .filter()
                    .select_related("category")
                    .prefetch_related("images", "tags")
                    )
        name = request.GET.get("name")
        if name:
            products = products.filter(title__icontains=name)

        min_price = request.GET.get("min_price")
        if min_price:
            products = products.filter(price__gte=min_price)

        max_price = request.GET.get("max_price")
        if max_price:
            products = products.filter(price__lte=max_price)

        free_delivery = request.GET.get("freeDelivery")
        if free_delivery is not None:
            products = products.filter(freeDelivery=free_delivery.lower() == "true")

        available = request.GET.get("available")
        if available is not None:
            if available.lower() == "true":
                products = products.filter(count__gt=0)

        pagination = paginate_queryset(products, request, per_page=8)
        serializer = ProductSerializer(pagination["items"], many=True)

        return Response({
            "items": serializer.data,
            "currentPage": pagination["currentPage"],
            "lastPage": pagination["lastPage"],
        })
