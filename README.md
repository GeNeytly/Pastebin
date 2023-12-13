# Pastebin

## Stack


docker compose exec web-app python manage.py collectstatic
# Статика приложения в контейнере backend 
# будет собрана в директорию /app/collected_static/.

# Теперь из этой директории копируем статику в /backend_static/static/;
# эта статика попадёт на volume static в папку /static/:
docker compose exec web-app cp -r /app/collected_static/. /backend_static/static/ 