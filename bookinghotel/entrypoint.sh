#!/bin/sh

echo "📦 Применяем миграции..."
python manage.py migrate

echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

echo "👤 Создаём суперпользователя, если не существует..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END

echo "🚀 Запуск Gunicorn..."
gunicorn bookinghotel.wsgi:application --bind 0.0.0.0:8000

