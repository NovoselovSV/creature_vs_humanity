# creature_vs_humanity
## Описание
Проект создан для тестирования взаимодействия различных библиотек и выполнен в виде игры про борьбу существ (creatures) и людей (humans).
## TODO
### Creatures
 - [ ] Доделать функциональность
    - [X] Получение ресурсов
    - [X] Повышение уровня существа
    - [X] Логика JWT auth
    - [ ] Логика атаки
### Humans
 - [ ] Структурно повторить функциональность creatures на FastAPI.
### Общее
 - [ ] Дополнить Readme.
 - [ ] Создать инфраструктуру на Docker.
 - [ ] Написать тесты функциональности.
 - [ ] Создать автоматизированное нагрузочное тестирование.
 - [ ] Опционально. Добавить возможность генерации описания с помощью локальной ИИ.
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
### Общее
 1. pytest
 2. faker
