from typing import TYPE_CHECKING

from django.db.models import Avg, Count, QuerySet

if TYPE_CHECKING:
    from app.catalog.models import Product


class CatalogDomainService:
    @staticmethod
    def apply_filters(queryset: QuerySet, filters: dict) -> QuerySet:
        if name := filters.get("name"):
            queryset = queryset.filter(title__icontains=name)
        if min_price := filters.get("minPrice"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := filters.get("maxPrice"):
            queryset = queryset.filter(price__lte=max_price)
        if filters.get("freeDelivery") == "true":
            queryset = queryset.filter(freeDelivery=True)
        if filters.get("available") == "true":
            queryset = queryset.filter(count__gt=0)
        if tags := filters.get("tags[]"):
            if not isinstance(tags, (list, tuple)):
                tags = [tags]
            queryset = queryset.filter(tags__id__in=tags).distinct()
        return queryset

    @staticmethod
    def apply_sorting(
        queryset: QuerySet,
        sort_field: str | None,
        sort_type: str | None,
    ) -> QuerySet:
        if sort_field:
            prefix = "" if sort_type == "inc" else "-"
            queryset = queryset.order_by(f"{prefix}{sort_field}")
        return queryset

    @staticmethod
    def recalculate_rating(product: Product) -> None:
        stats = product.review_list.aggregate(
            reviews_count=Count("id"), avg_rating=Avg("rate")
        )
        product.reviews = stats["reviews_count"] or 0
        product.rating = round(stats["avg_rating"] or 0, 1)
        product.save(update_fields=["reviews", "rating"])
