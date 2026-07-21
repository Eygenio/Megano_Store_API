from django.http import HttpRequest

from app.basket.application.use_cases import (
    AddToBasketUseCase,
    CalculateBasketTotalUseCase,
    ClearBasketUseCase,
    GetBasketUseCase,
    MergeBasketsUseCase,
    RemoveFromBasketUseCase,
)
from app.basket.domain.services import BasketDomainService
from app.basket.infrastructure.repositories import (
    BasketRepository,
    SessionBasketRepository,
)


class BasketUseCaseFactory:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self._domain_service: BasketDomainService | None = None
        self._user_repo: BasketRepository | None = None
        self._session_repo: SessionBasketRepository | None = None

    @property
    def domain_service(self) -> BasketDomainService:
        if self._domain_service is None:
            self._domain_service = BasketDomainService()
        return self._domain_service

    @property
    def user_repo(self) -> BasketRepository:
        if self._user_repo is None:
            self._user_repo = BasketRepository()
        return self._user_repo

    @property
    def session_repo(self) -> SessionBasketRepository:
        if self._session_repo is None:
            self._session_repo = SessionBasketRepository(self.request.session)
        return self._session_repo

    def create_add_to_basket(self) -> AddToBasketUseCase:
        return AddToBasketUseCase(
            domain_service=self.domain_service,
            user_repo=self.user_repo,
            session_repo=self.session_repo,
        )

    def create_remove_from_basket(self) -> RemoveFromBasketUseCase:
        return RemoveFromBasketUseCase(
            domain_service=self.domain_service,
            user_repo=self.user_repo,
            session_repo=self.session_repo,
        )

    def create_get_basket(self) -> GetBasketUseCase:
        return GetBasketUseCase(
            user_repo=self.user_repo,
            session_repo=self.session_repo,
        )

    def create_clear_basket(self) -> ClearBasketUseCase:
        return ClearBasketUseCase(
            user_repo=self.user_repo,
            session_repo=self.session_repo,
        )

    def create_merge_baskets(self) -> MergeBasketsUseCase:
        return MergeBasketsUseCase(
            domain_service=self.domain_service,
            user_repo=self.user_repo,
            session_repo=self.session_repo,
        )

    def create_calculate_total(self) -> CalculateBasketTotalUseCase:
        return CalculateBasketTotalUseCase(
            domain_service=self.domain_service,
        )
