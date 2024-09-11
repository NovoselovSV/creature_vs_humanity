# creature_vs_humanity
## Описание
Проект представляет собой игру про борьбу существ (creatures) и людей (humans). "Существа" созданы на основе фреймворка Django, а "люди" - FastAPI.
## Установка и запуск
 1. Клонировать репозиторий
```bash
git clone https://github.com/NovoselovSV/creature_vs_humanity.git
```
 2. Создать, активировать виртуальное окружение и установить зависимости для:

   1. части creatures
```bash
cd path/to/repo/creatures
```
```bash
python3 -m venv venv
```
```bash
source env/bin/activate
```
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

   2. части humans
```bash
cd path/to/repo/humans
```
```bash
python3 -m venv venv
```
```bash
source env/bin/activate
```
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

 3. Запуск проекта (каждое действие производить в отдельной сессии оболочки):

   1. часть creatures

     1. Запуск redis-server(если не запущен)
```bash
redis-server
```

     2. Запуск приложения
```bash
python manage.py runserver
```

     3. Запуск celery worker
```bash
celery -A creatures worker [-l info]
```

   2. часть humans

     1. Запуск redis-server(если не запущен)
```bash
redis-server
```

     2. Запуск приложения
```bash
uvicorn main:app [--reload] --port 8001
```

     3. Запуск celery worker
```bash
celery -A celery_app.celery_app worker [-l info]
```

## Использованные технологии

### Creatures
 1. Django
 2. DRF
 3. Redis
 4. Celery

### Humans
 1. FastAPI
 2. SQLAlchemy
 3. Redis
 4. Celery

## Автор
[Новоселов Сергей](https://github.com/NovoselovSV)
