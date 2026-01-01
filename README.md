# 🛒 Megano Store API v1.0.0 — Django + DRF + PostgreSQL + Docker

Backend-приложение интернет-магазина, реализующее каталог товаров, корзину, заказы, оплату и пользователей.  
Проект выполнен в виде модульной Django-архитектуры с REST API и поддержкой Docker.

---

## ✨ Возможности

* 🧑 Пользователи и аутентификация
* 🗂 Каталог товаров и категорий
* 🏷 Теги, скидки и фильтрация
* 🛒 Корзина (session + DB)
* 📦 Заказы и позиции заказа
* 💳 Оплата заказов
* 🖼 Медиафайлы (изображения товаров)
* 🛠 Админ-панель Django
* 🐳 Полная поддержка Docker + docker-compose
* 📡 REST API (Django REST Framework)

---

## 🏗️ Архитектура проекта

```
project/
├── megano/
│   ├── app/
│   │ ├── basket/
│   │ │ ├── models.py
│   │ │ ├── services.py
│   │ │ ├── serializers.py   
│   │ │ ├── tests.py
│   │ │ ├── urls.py
│   │ │ ├── utils.py
│   │ │ └── views.py
│   │ ├── catalog/
│   │ │ ├── models.py
│   │ │ ├── serializers.py
│   │ │ ├── tests.py
│   │ │ ├── urls.py
│   │ │ └── views.py    
│   │ ├── core/
│   │ │ └── management/
│   │ │ │   └── commands/
│   │ │ │       └── initdata.py
│   │ │ ├── models.py
│   │ │ ├── pagination.py
│   │ │ └── serializers.py    
│   │ ├── orders/
│   │ │ ├── models.py
│   │ │ ├── serializers.py
│   │ │ ├── tests.py
│   │ │ ├── urls.py
│   │ │ └── views.py 
│   │ ├── payment/
│   │ │ ├── models.py
│   │ │ ├── serializers.py
│   │ │ ├── urls.py
│   │ │ └── views.py 
│   │ ├── users/
│   │ │ ├── auth_urls.py
│   │ │ ├── models.py
│   │ │ ├── serializers.py   
│   │ │ ├── urls.py
│   │ │ ├── utils.py
│   │ │ └── views.py
│   │ └── utils/
│   ├── config/
│   │ ├── settings/
│   │ │ ├── base.py
│   │ │ ├── dev.py
│   │ │ └── prod.py
│   │ ├── urls.py
│   │ ├── wsgi.py
│   │ └── asgi.py
│   ├── media/
│
├── diploma-frontend/
├── Dockerfile
├── docker-compose.yaml
├── entrypoint.sh
├── .env
├── manage.py
├── requirements.txt
└── README.md

```

---

## 🧰 Используемые технологии

* Python 3.13
* Django 6
* Django REST Framework
* PostgreSQL
* WhiteNoise (static files)
* Docker / docker-compose
* Pytest

---

## 💡 Функциональность

### 👤 Пользователи

* регистрация
* аутентификация
* профиль пользователя

---

### 🗂 Каталог

* категории
* товары
* теги
* изображения товаров
* скидки
* фильтрация и сортировка

---

### 🛒 Корзина

* добавление / удаление товаров
* хранение в session и базе
* подсчёт стоимости

---

### 📦 Заказы

* оформление заказа
* позиции заказа
* история заказов пользователя
* расчёт итоговой стоимости

---

### 💳 Оплата

* проверка платежного кода
* симуляция оплаты заказа
* изменение статуса заказа

---

# 🚀 Запуск проекта (локально)

## 1. Клонировать репозиторий

```bash
git clone https://github.com/Eygenio/Megano_Store_API.git
```

## 2. Создать `.env` или скопируйте содержимое `.env.template` в `.env`

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=
```

## 3. 🐳 Сборка через Docker

```bash
docker-compose build
```

## 4. 🐳 Запуск через Docker

```bash
docker-compose up -d
```

## 🔗 Доступ к сервису

```bash
http://0.0.0.0:8080/ 
```

## 🔗 Доступ к "Админке"

```bash
http://0.0.0.0:8080/admin/
```

---

# 🔐 Безопасность

* DEBUG = False в production
* PostgreSQL изолирован Docker'ом
* WhiteNoise для безопасной раздачи статики
* Переменные окружения через `.env`
