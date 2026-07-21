from dataclasses import dataclass

from app.catalog.constants import LIMIT_POPULAR_PRODUCT, LIMIT_PRODUCT, SALES_PER_PAGE
from app.catalog.domain.exceptions import ProductNotFoundError
from app.catalog.domain.services import CatalogDomainService
from app.catalog.dto import CatalogRequestDTO, ReviewDataDTO
from app.catalog.infrastructure.repositories import (
    CategoryRepository,
    ProductRepository,
    ReviewRepository,
    SalesRepository,
    TagRepository,
)
from app.catalog.models import Product
from app.core.pagination import paginate_queryset


@dataclass
class GetCatalogUseCase:
    product_repo: ProductRepository

    def execute(self, request_dto: CatalogRequestDTO) -> dict:
        filters = {
            "name": request_dto.filters.name,
            "minPrice": request_dto.filters.min_price,
            "maxPrice": request_dto.filters.max_price,
            "freeDelivery": request_dto.filters.free_delivery,
            "available": request_dto.filters.available,
            "tags[]": request_dto.filters.tags,
        }
        filters = {k: v for k, v in filters.items() if v is not None and v != ""}

        qs = self.product_repo.get_catalog(
            filters,
            request_dto.sorting.sort_field,
            request_dto.sorting.sort_type,
        )
        pagination = paginate_queryset(qs, request_dto.page)
        return {
            "items": list(pagination["items"]),
            "currentPage": pagination["currentPage"],
            "lastPage": pagination["lastPage"],
        }


@dataclass
class GetProductUseCase:
    product_repo: ProductRepository

    def execute(self, product_id: int) -> Product:
        try:
            return self.product_repo.get_by_id(product_id)
        except Product.DoesNotExist as err:
            raise ProductNotFoundError(
                f"Product with id {product_id} not found."
            ) from err


@dataclass
class AddReviewUseCase:
    domain_service: CatalogDomainService
    review_repo: ReviewRepository
    product_repo: ProductRepository

    def execute(self, product_id: int, review_dto: ReviewDataDTO) -> dict:
        product = self.product_repo.get_by_id(product_id)
        review_data = {
            "author": review_dto.author,
            "email": review_dto.email,
            "text": review_dto.text,
            "rate": review_dto.rate,
        }
        self.review_repo.create_review(product, review_data)
        self.domain_service.recalculate_rating(product)
        return review_data


@dataclass
class GetCategoriesUseCase:
    category_repo: CategoryRepository

    def execute(self) -> list:
        return list(self.category_repo.get_tree())


@dataclass
class GetPopularProductsUseCase:
    product_repo: ProductRepository

    def execute(self, limit: int = LIMIT_POPULAR_PRODUCT) -> list:
        return list(self.product_repo.get_popular(limit))


@dataclass
class GetLimitedProductsUseCase:
    product_repo: ProductRepository

    def execute(self, limit: int = LIMIT_PRODUCT) -> list:
        return list(self.product_repo.get_limited(limit))


@dataclass
class GetSalesUseCase:
    sales_repo: SalesRepository

    def execute(self, page: int, per_page: int = SALES_PER_PAGE) -> dict:
        qs = self.sales_repo.get_active_sales()
        pagination = paginate_queryset(qs, page, per_page)
        return {
            "items": list(pagination["items"]),
            "currentPage": pagination["currentPage"],
            "lastPage": pagination["lastPage"],
        }


@dataclass
class GetBannersUseCase:
    product_repo: ProductRepository

    def execute(self) -> list:
        return list(self.product_repo.get_banners())


@dataclass
class GetTagsUseCase:
    tag_repo: TagRepository

    def execute(self) -> list:
        return list(self.tag_repo.get_all())
