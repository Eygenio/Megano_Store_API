class CatalogDomainError(Exception):
    pass


class ProductNotFoundError(CatalogDomainError):
    pass
