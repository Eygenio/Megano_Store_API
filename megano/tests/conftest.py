from datetime import date

import pytest
from app.catalog.models import Category, Product, Sales, Tag
from app.orders.models import DeliverySettings
from app.users.models import User
from faker import Faker
from rest_framework.test import APIClient

fake = Faker()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def basket_url() -> str:
    return "/api/basket/"


@pytest.fixture
def catalog_url() -> str:
    return "/api/catalog/"


@pytest.fixture
def categories_url() -> str:
    return "/api/categories/"


@pytest.fixture
def orders_url() -> str:
    return "/api/orders/"


@pytest.fixture
def payment_url() -> str:
    return "/api/payment/"


@pytest.fixture
def sign_in_url() -> str:
    return "/api/sign-in/"


@pytest.fixture
def sign_up_url() -> str:
    return "/api/sign-up/"


@pytest.fixture
def user_password() -> str:
    return "testpass123"


@pytest.fixture
def user(user_password: str) -> User:
    return User.objects.create_user(
        username=fake.user_name(),
        password=user_password,
    )


@pytest.fixture
def category() -> Category:
    return Category.objects.create(title=fake.word())


@pytest.fixture
def second_category() -> Category:
    return Category.objects.create(title=fake.word())


@pytest.fixture
def tag() -> Tag:
    return Tag.objects.create(name=fake.word())


@pytest.fixture
def product(category: Category) -> Product:
    return Product.objects.create(
        category=category,
        price=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
        count=fake.random_int(min=1, max=100),
        title=fake.word().capitalize(),
        description=fake.sentence(),
        freeDelivery=fake.boolean(),
    )


@pytest.fixture
def second_product(second_category: Category) -> Product:
    return Product.objects.create(
        category=second_category,
        price=fake.pydecimal(left_digits=1, right_digits=2, positive=True),
        count=fake.random_int(min=1, max=50),
        title=fake.word().capitalize(),
        freeDelivery=False,
    )


@pytest.fixture
def limited_product(category: Category) -> Product:
    return Product.objects.create(
        category=category,
        price=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
        count=fake.random_int(min=1, max=10),
        title=fake.word().capitalize(),
        limited=True,
    )


@pytest.fixture
def sale_product(product: Product) -> Sales:
    return Sales.objects.create(
        product=product,
        salePrice=fake.pydecimal(left_digits=1, right_digits=2, positive=True),
        dateFrom=date.today(),
        dateTo=date.today(),
    )


@pytest.fixture
def delivery_settings() -> None:
    DeliverySettings.objects.get_or_create(
        free_delivery_threshold=fake.random_int(min=100, max=1000),
        delivery_price=fake.random_int(min=5, max=50),
        express_delivery_price=fake.random_int(min=20, max=100),
    )


@pytest.fixture
def authenticated_client(api_client: APIClient, user: User) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def payment_payload() -> dict:
    return {
        "number": fake.credit_card_number(),
        "name": fake.name(),
        "month": fake.month(),
        "year": str(fake.year()),
        "code": fake.credit_card_security_code(),
    }


@pytest.fixture
def sign_up_payload() -> dict:
    return {
        "username": fake.user_name(),
        "password": fake.password(length=10),
        "email": fake.email(),
        "phone": fake.phone_number()[:20],
        "fullname": fake.name(),
    }


@pytest.fixture
def order_payload() -> dict:
    return {
        "deliveryType": "standard",
        "city": fake.word(),
        "address": fake.word(),
    }
