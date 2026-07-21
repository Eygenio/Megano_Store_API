from dataclasses import dataclass, field


@dataclass(frozen=True)
class CatalogFiltersDTO:
    name: str | None = None
    min_price: str | None = None
    max_price: str | None = None
    free_delivery: str | None = None
    available: str | None = None
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CatalogSortingDTO:
    sort_field: str | None = None
    sort_type: str | None = None


@dataclass(frozen=True)
class CatalogRequestDTO:
    filters: CatalogFiltersDTO
    sorting: CatalogSortingDTO
    page: int = 1


@dataclass(frozen=True)
class ReviewDataDTO:
    author: str
    email: str
    text: str
    rate: int
