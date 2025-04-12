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
   git clone https://github.com/username/tweet-api.git
2. Настройка контейнеров
    ```bash
   docker compose build
3. Подготовка БД и миграций
    ```bash
   docker compose up -d db  # запуска контейнера БД в фоновом режиме
   docker compose run api alembic revision --autogenerate -m "Initial migration" # Создаем начальную миграцию
   docker compose run api alembic upgrade head # применяем созданную миграцию
4. Запуск приложения
    ```bash   
   docker compose up  

## Документация API
Swagger UI : http://localhost:8000/docs