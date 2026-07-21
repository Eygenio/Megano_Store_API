from typing import TYPE_CHECKING

from app.catalog.domain.services import CatalogDomainService
from app.catalog.models import Category, Product, Review, Sales, Tag

if TYPE_CHECKING:
    from django.db.models import QuerySet


class ProductRepository:
    def get_base_queryset(self) -> QuerySet:
        return (
            Product.objects.select_related("category")
            .prefetch_related("images", "tags")
            .order_by("id")
        )

    def get_by_id(self, product_id: int) -> Product:
        return (
            Product.objects.select_related("category")
            .prefetch_related("images", "tags", "specifications", "review_list")
            .get(id=product_id)
        )

    def get_catalog(
        self,
        filters: dict,
        sort_field: str | None,
        sort_type: str | None,
    ) -> QuerySet:
        qs = self.get_base_queryset()
        qs = CatalogDomainService.apply_filters(qs, filters)
        qs = CatalogDomainService.apply_sorting(qs, sort_field, sort_type)
        return qs

    def get_popular(self, limit: int = 8) -> QuerySet:
        return self.get_base_queryset().order_by("sortIndex", "-purchases")[:limit]

    def get_limited(self, limit: int = 16) -> QuerySet:
        return self.get_base_queryset().filter(limited=True)[:limit]

    def get_banners(self) -> QuerySet:
        return self.get_base_queryset().filter(freeDelivery=True)


class CategoryRepository:
    def get_tree(self) -> QuerySet:
        return (
            Category.objects.filter(parent__isnull=True)
            .select_related("image")
            .prefetch_related("subcategories__image")
            .order_by("title")
        )


class ReviewRepository:
    def create_review(self, product: Product, data: dict) -> Review:
        return Review.objects.create(product=product, **data)


class SalesRepository:
    def get_active_sales(self) -> QuerySet:
        return Sales.objects.select_related("product").all().order_by("product_id")


class TagRepository:
    def get_all(self) -> QuerySet:
        return Tag.objects.all()
