Django-ZEN

Проект API для платформы, похожей на Яндекс.Дзен
Реализованы *RUD операции для постов, комментариев, авторизация и оценки публикаций.  

Стек технологий

Backend Django, Django REST Framework  
База данных PostgreSQL  
Очереди и фоновые задачи Celery + RabbitMQ  
Тестирование Pytest  
DevOps Docker, Docker Compose, GitHub Actions (CI/CD)  
Парсинг requests
Уведомления Telegram Bot API, Email Backend  


Установка и запуск проекта

Клонируем репозиторий  

python -m venv venv

загружаем все зависимости
pip install -r requirements.txt

строго создат файл .env после прописат заполнит все переменные
# dev-db
USER=your_user
NAME=your_db_name
HOST=localhost
PORT=5432
PASSWORD=your_password
DATABASE_URL=postgresql://your_user:your_password@db:5432/your_db_name

# test-db
TEST_DB_NAME=your_test_db
TEST_DATABASE_URL=postgresql://your_user:your_password@test-db:5432/your_test_db

# Django settings
SECRET_KEY=your_django_secret_key

# Telegram bot
TELEGRAM_BOT_TOKEN=your_bot_token
BOT_USERNAME=your_bot_username


Запуск компоса, происходит авто тесты затем поднимается сервер
docker-compose -f docker-compose.local.yaml up --build -d

Создание супер пользователя
docker exec -it web python manage.py createsuperuser

CI/CD
Проект поддерживает автоматический деплой с использованием GitHub Actions.
Каждый push в develop = Работа тестов, push в main = Начинается процесс делпойя
Запускает тесты
Собирает контейнеры
Деплоит проект на сервер
