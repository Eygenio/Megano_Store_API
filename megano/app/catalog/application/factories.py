from app.catalog.application.use_cases import (
    AddReviewUseCase,
    GetBannersUseCase,
    GetCatalogUseCase,
    GetCategoriesUseCase,
    GetLimitedProductsUseCase,
    GetPopularProductsUseCase,
    GetProductUseCase,
    GetSalesUseCase,
    GetTagsUseCase,
)
from app.catalog.domain.services import CatalogDomainService
from app.catalog.infrastructure.repositories import (
    CategoryRepository,
    ProductRepository,
    ReviewRepository,
    SalesRepository,
    TagRepository,
)


class CatalogUseCaseFactory:
    def __init__(self):
        self._product_repo = None
        self._category_repo = None
        self._review_repo = None
        self._sales_repo = None
        self._tag_repo = None
        self._domain_service = None

    @property
    def product_repo(self) -> ProductRepository:
        if self._product_repo is None:
            self._product_repo = ProductRepository()
        return self._product_repo

    @property
    def category_repo(self) -> CategoryRepository:
        if self._category_repo is None:
            self._category_repo = CategoryRepository()
        return self._category_repo

    @property
    def review_repo(self) -> ReviewRepository:
        if self._review_repo is None:
            self._review_repo = ReviewRepository()
        return self._review_repo

    @property
    def sales_repo(self) -> SalesRepository:
        if self._sales_repo is None:
            self._sales_repo = SalesRepository()
        return self._sales_repo

    @property
    def tag_repo(self) -> TagRepository:
        if self._tag_repo is None:
            self._tag_repo = TagRepository()
        return self._tag_repo

    @property
    def domain_service(self) -> CatalogDomainService:
        if self._domain_service is None:
            self._domain_service = CatalogDomainService()
        return self._domain_service

    def create_get_catalog(self) -> GetCatalogUseCase:
        return GetCatalogUseCase(product_repo=self.product_repo)

    def create_get_product(self) -> GetProductUseCase:
        return GetProductUseCase(product_repo=self.product_repo)

    def create_add_review(self) -> AddReviewUseCase:
        return AddReviewUseCase(
            domain_service=self.domain_service,
            review_repo=self.review_repo,
            product_repo=self.product_repo,
        )

    def create_get_categories(self) -> GetCategoriesUseCase:
        return GetCategoriesUseCase(category_repo=self.category_repo)

    def create_get_popular_products(self) -> GetPopularProductsUseCase:
        return GetPopularProductsUseCase(product_repo=self.product_repo)

    def create_get_limited_products(self) -> GetLimitedProductsUseCase:
        return GetLimitedProductsUseCase(product_repo=self.product_repo)

    def create_get_sales(self) -> GetSalesUseCase:
        return GetSalesUseCase(sales_repo=self.sales_repo)

    def create_get_banners(self) -> GetBannersUseCase:
        return GetBannersUseCase(product_repo=self.product_repo)

    def create_get_tags(self) -> GetTagsUseCase:
        return GetTagsUseCase(tag_repo=self.tag_repo)
