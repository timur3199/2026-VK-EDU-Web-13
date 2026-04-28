# AskMe — платформа вопросов и ответов

## Быстрый старт (локально, SQLite)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cp .env.example .env.local
python manage.py migrate
python manage.py createsuperuser
python manage.py fill_db 100   # заполнить тестовыми данными
python manage.py runserver
```

Открыть: http://127.0.0.1:8000/ | Админка: http://127.0.0.1:8000/admin/

## Запуск через Docker Compose (PostgreSQL)

```bash
docker compose up --build
```

После запуска:
```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py fill_db 100
```

## Команда заполнения БД

```bash
python manage.py fill_db [ratio]
```

| ratio | Пользователи | Вопросы | Ответы | Теги | Лайки |
|-------|-------------|---------|--------|------|-------|
| 1     | 1           | 10      | 100    | 1    | 200   |
| 100   | 100         | 1 000   | 10 000 | 100  | 20 000|
| 10000 | 10 000      | 100 000 | 1 000 000 | 10 000 | 2 000 000 |
