# AskMe — платформа вопросов и ответов

Учебный проект в рамках курса VK Education Web.

## Структура проекта

```
askme/
├── application/        # Настройки Django (settings, urls, wsgi)
├── core/               # Приложение: логин, регистрация, профиль
│   └── templates/core/
├── questions/          # Приложение: вопросы и ответы
│   └── templates/questions/
├── templates/          # Общие шаблоны (base.html, includes/)
├── static/             # CSS, JS, изображения
├── media/              # Загружаемые пользователем файлы
├── manage.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Страницы

| URL | Описание |
|-----|----------|
| `/` | Список новых вопросов |
| `/hot/` | Список популярных вопросов |
| `/tag/<tag>/` | Вопросы по тегу |
| `/question/<id>/` | Страница вопроса с ответами |
| `/ask/` | Форма создания вопроса |
| `/login/` | Вход |
| `/signup/` | Регистрация |
| `/profile/` | Редактирование профиля |
