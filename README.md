# API-сервис бронирования столиков в ресторане

## Описание проекта
Сервис позволяет создавать, просматривать и удалять брони, а также управлять столиками и временными слотами.

## Технологии
- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy** - ORM для работы с БД
- **Docker** - контейнеризация приложения
- **Alembic** - управление миграциями
- **Pytest** - модульное тестирование

## Установка и запуск

### Предварительные требования
1. Docker и Docker Compose должны быть установлены
2. Python 3.12

### Запуск проекта
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/davidoganesyan/booking_api
2. Настройка контейнеров
    ```bash
   docker compose build
3. Запуск контейнера БД в фоновом режиме
    ```bash
   docker compose up -d db
4. Создание начальной миграции
    ```bash
   docker compose run api alembic revision --autogenerate -m "Initial migration"
5. Применяем начальную миграцию
    ```bash
   docker compose run api alembic upgrade head
6. Запуск приложения
    ```bash   
   docker compose up  

## Документация API
Swagger UI : http://localhost:8000/docs