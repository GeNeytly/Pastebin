# Pastebin

## Stack
- Python 3.9
- Django 4.2.6
- Django Rest Framework 3.14.0
- Postgres 13.10
- Nginx 1.22.1
- Redis 7.0.5
- Celery 5.3.6
- Flower 2.0.1


docker compose exec web-app python manage.py collectstatic
# Статика приложения в контейнере backend 
# будет собрана в директорию /app/collected_static/.

# Теперь из этой директории копируем статику в /backend_static/static/;
# эта статика попадёт на volume static в папку /static/:
docker compose exec web-app cp -r /app/collected_static/. /backend_static/static/ 