# 🛒 Megano Store API v1.0.0 — Django + DRF + PostgreSQL + Docker

Backend for an online store: product catalog, shopping cart, orders, payments, and user management.  
Built with a modular Django architecture, REST API, and full Docker support.

> ⚠️ The project implements the **backend only**.  
> The frontend is provided as a ready-made package and was used for API integration and testing.

---

## ✨ Features

* 👤 Users & authentication  
* 🗂 Product catalog with categories  
* 🏷 Tags, discounts, filtering & sorting  
* 🛒 Shopping cart (session-based and DB-backed)  
* 📦 Orders with line items  
* 💳 Order payment simulation  
* 🖼 Media files (product images)  
* 🛠 Django admin panel  
* 🐳 Full Docker & docker-compose support  
* 🧪 Automated tests (unit, integration, e2e)  
* 🌐 Nginx reverse proxy for static/media and proxying to Gunicorn  
* 📦 Dependency management with `uv`  
* 🧹 Code quality tools: `black`, `isort`, `flake8`, `mypy`  
* 📝 Structured logging with `colorlog`

---

## 🏗️ Architecture

The project follows **Clean Architecture** principles with clear separation of concerns:

* **Domain** – pure business logic, no framework dependencies  
* **Application** – use cases orchestrating domain services and repositories  
* **Infrastructure** – Django ORM repositories and other external concerns  
* **Interfaces** – DRF views, serializers, and URL routing  
* **DTOs** – explicit data transfer objects between layers  
* **Constants** – shared values extracted into dedicated modules 

```
project/
├── megano/
│   ├── app/
│   │ ├── basket/
│   │ │ ├── domain
│   │ │ ├── application
│   │ │ ├── infrastructure   
│   │ │ └── interfaces
│   │ ├── catalog/ 
│   │ ├── core/  
│   │ ├── orders/
│   │ ├── payment/
│   │ ├── users/
│   │ └── utils/
│   ├── config/
│   ├── media/
│   └── tests/
├── diploma-frontend/
├── Dockerfile
├── docker-compose.yaml
├── .env
├── manage.py
└── README.md

```

---

## 🧰 Technology Stack

* Python 3.13
* Django 6.0
* Django REST Framework
* PostgreSQL
* Gunicorn 
* Nginx  
* WhiteNoise
* Docker / docker-compose
* `uv` (dependency management)  
* Pytest (with markers for unit / integration / e2e)  
* `mypy`, `flake8`, `black`, `isort`

---

## 💡 Functionality

### 👤 Users

* Registration 
* Authentication (session-based)  
* Profile & avatar management  

---

### 🗂 Catalog

* Categories (tree)  
* Products with images, tags, descriptions  
* Sales / discounts 
* Filtering, sorting, and pagination  

---

### 🛒 Cart

* Add / remove items  
* Support for both anonymous (session) and authenticated (DB) users
* Price calculation  

---

### 📦 Orders

* Order creation from basket  
* Order history  
* Delivery cost calculation  
* Status management 

---

### 💳 Payment

* Payment simulation (card data validation)  
* Transaction ID generation  
* Order status update  

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/Eygenio/Megano_Store_API.git
```

## 2. Create a `.env` file (or copy the template)

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

DJANGO_SETTINGS_MODULE=
DJANGO_ALLOWED_HOSTS=
DJANGO_SECRET_KEY=

DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=
```

## 3. 🐳 Build & run with Docker

```bash
docker-compose build
docker-compose up -d
```
The application will be available at `http://0.0.0.0:8080/`.
The admin panel is at `http://0.0.0.0:8080/admin/`.

---
# 🧪 Testing

Tests are located in the tests/ folder and are organized by scope:

* Unit – domain services, pure logic
* Integration – API endpoints with test database
* E2E – complete user workflows

Run all tests:
```bash
pytest -v
```

---

# 🧹 Code Quality
The project enforces consistent code style and type checking:

```bash
black .          # code formatting
isort .          # import sorting
flake8 megano    # linting
mypy megano      # static type checking
```

---

# 🔐 Security

* `DEBUG = False` in production (managed via environment)
* PostgreSQL isolated inside Docker
* WhiteNoise serves static files efficiently
* All sensitive data is stored in environment variables
* Nginx acts as a reverse proxy and serves media files

