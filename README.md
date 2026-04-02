# AskMe — Q&A платформа

Учебный проект. Статическая вёрстка сайта вопросов и ответов для разработчиков.

## Страницы

| Файл | Маршрут | Описание |
|------|---------|----------|
| `index.html` | `/` | Список вопросов |
| `question.html` | `/question/<id>/` | Страница вопроса с ответами |
| `ask.html` | `/ask/` | Форма создания вопроса |
| `tag.html` | `/tag/<name>/` | Вопросы по тегу |
| `login.html` | `/login/` | Вход |
| `signup.html` | `/signup/` | Регистрация |
| `profile.html` | `/profile/` | Настройки профиля |

## Структура

```
public/
├── base.html
├── index.html
├── question.html
├── ask.html
├── tag.html
├── login.html
├── signup.html
├── profile.html
└── static/
    ├── css/
    │   ├── reset.css
    │   ├── bootstrap.min.css
    │   └── style.css
    ├── js/
    │   ├── bootstrap.bundle.min.js
    │   └── main.js
    └── img/
```
