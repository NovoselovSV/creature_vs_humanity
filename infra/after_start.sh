#!/bin/bash
sudo docker compose exec creatures python manage.py migrate
sudo docker compose exec creatures python manage.py collectstatic
sudo docker compose exec creatures cp -r /app/collected_static/. /creatures_static/static/
sudo docker compose exec humans alembic upgrade head
sudo docker compose exec creatures python manage.py createsuperuser
sudo docker compose exec humans python commands.py
