from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# ─── Pagination helper ────────────────────────────────────────────────────────

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


# ─── Stub data ────────────────────────────────────────────────────────────────

TAGS = ['python', 'javascript', 'django', 'react', 'postgresql',
        'docker', 'api', 'sql', 'css', 'linux']

MEMBERS = [
    {'initials': 'АП', 'name': 'aleksey_p', 'score': 842},
    {'initials': 'МК', 'name': 'maria_k',   'score': 719},
    {'initials': 'ИС', 'name': 'ivan_s',    'score': 634},
    {'initials': 'ДВ', 'name': 'dmitry_v',  'score': 571},
    {'initials': 'НО', 'name': 'natasha_o', 'score': 498},
]

QUESTION_TITLES = [
    'Как правильно использовать prefetch_related и select_related в Django ORM?',
    'Разница между Promise и async/await в JavaScript?',
    'Как настроить Docker Compose для Django + PostgreSQL?',
    'Что такое индексы в PostgreSQL и когда их использовать?',
    'Как реализовать JWT-аутентификацию в DRF?',
    'В чём разница между useEffect и useLayoutEffect в React?',
    'Как сделать пагинацию в Django REST Framework?',
    'Почему Git говорит «detached HEAD»?',
    'Как оптимизировать медленные SQL-запросы?',
    'Что такое SOLID и зачем это нужно?',
    'Как работает event loop в Node.js?',
    'Как правильно хранить секреты в переменных окружения?',
    'Разница между margin и padding в CSS?',
    'Как сделать деплой Django на Linux-сервер?',
    'Что такое WebSocket и когда его использовать?',
    'Как работают транзакции в базах данных?',
    'Что такое Big O нотация?',
    'Как настроить Celery с Django?',
    'В чём разница между REST и GraphQL?',
    'Как писать юнит-тесты для Django views?',
    'Что такое контекстные менеджеры в Python?',
    'Как работает GIL в Python?',
    'Как сделать горизонтальное масштабирование приложения?',
    'Разница между TCP и UDP?',
    'Как правильно структурировать большой Django-проект?',
    'Что такое мемоизация и как её применять?',
    'Как настроить CORS в Django?',
    'Что такое дескрипторы в Python?',
    'Как работает кэширование в Django?',
    'В чём разница между list и tuple в Python?',
]

EXCERPTS = [
    'Столкнулся с проблемой N+1 запросов. Как определить, когда использовать prefetch_related?',
    'Пробовал оба подхода, но не понимаю ключевых отличий в реальных сценариях.',
    'Контейнеры запускаются, но Django не может подключиться к базе данных.',
    'Слышал, что индексы ускоряют запросы, но не знаю, где их создавать.',
    'Нужно реализовать авторизацию без сессий, какой подход выбрать?',
    'Мой useEffect работает не так, как ожидалось при рендере.',
    'Нужно отдавать данные постранично через API.',
    'После переключения между ветками Git перешёл в странное состояние.',
    'Запросы занимают несколько секунд, нужно понять как их ускорить.',
    'Коллеги постоянно упоминают SOLID, но что это значит на практике?',
]

QUESTION_TAGS = [
    ['django', 'python', 'orm'],
    ['javascript', 'async'],
    ['docker', 'django', 'postgresql'],
    ['postgresql', 'sql'],
    ['django', 'api', 'python'],
    ['react', 'javascript'],
    ['django', 'api'],
    ['git'],
    ['sql', 'postgresql'],
    ['python', 'architecture'],
]

ANSWER_TEXTS = [
    'Отличный вопрос! select_related работает с ForeignKey через JOIN, а prefetch_related — с ManyToMany через отдельный запрос.',
    'Это классическая проблема. Попробуйте добавить explain analyze к вашему запросу.',
    'Рекомендую изучить официальную документацию и попробовать на небольшом примере.',
    'Суть в том, что нужно смотреть на конкретный use case и измерять производительность.',
    'Я сталкивался с похожей проблемой. Решение оказалось простым — нужно проверить настройки.',
]


def make_questions(count=30, hot=False):
    questions = []
    for i in range(1, count + 1):
        idx = (i - 1) % len(QUESTION_TITLES)
        tidx = (i - 1) % len(QUESTION_TAGS)
        eidx = (i - 1) % len(EXCERPTS)
        questions.append({
            'id': i,
            'title': QUESTION_TITLES[idx],
            'excerpt': EXCERPTS[eidx],
            'tags': QUESTION_TAGS[tidx],
            'author': 'user_' + str(i),
            'author_initials': 'U' + str(i),
            'created_at': f'{i} мин. назад' if i < 60 else f'{i // 60} ч. назад',
            'likes': (i * 7 + 3) % 50 if hot else (i * 2) % 20,
            'answers_count': (i * 3) % 10,
        })
    if hot:
        questions.sort(key=lambda q: q['likes'], reverse=True)
    return questions


def make_answers(count=5, question_id=1):
    answers = []
    for i in range(1, count + 1):
        answers.append({
            'id': i,
            'text': ANSWER_TEXTS[(i - 1) % len(ANSWER_TEXTS)],
            'author': 'answer_user_' + str(i),
            'author_initials': 'AU',
            'created_at': f'{i * 10} мин. назад',
            'likes': (i * 5) % 30,
            'is_correct': i == 2,
        })
    return answers


def base_context():
    return {'tags': TAGS, 'members': MEMBERS}


# ─── Views ────────────────────────────────────────────────────────────────────

def index(request):
    questions = make_questions(30, hot=False)
    page = paginate(questions, request, per_page=5)
    ctx = base_context()
    ctx.update({'page_obj': page, 'title': 'Новые вопросы', 'active_tab': 'new'})
    return render(request, 'questions/index.html', ctx)


def hot(request):
    questions = make_questions(30, hot=True)
    page = paginate(questions, request, per_page=5)
    ctx = base_context()
    ctx.update({'page_obj': page, 'title': 'Лучшие вопросы', 'active_tab': 'hot'})
    return render(request, 'questions/hot.html', ctx)


def tag(request, tag_name):
    all_questions = make_questions(30)
    questions = [q for q in all_questions if tag_name in q['tags']] or all_questions[:15]
    page = paginate(questions, request, per_page=5)
    ctx = base_context()
    ctx.update({'page_obj': page, 'tag_name': tag_name})
    return render(request, 'questions/tag.html', ctx)


def question(request, question_id):
    q = {
        'id': question_id,
        'title': QUESTION_TITLES[(question_id - 1) % len(QUESTION_TITLES)],
        'text': 'Подробное описание вопроса. ' + EXCERPTS[(question_id - 1) % len(EXCERPTS)] * 3,
        'tags': QUESTION_TAGS[(question_id - 1) % len(QUESTION_TAGS)],
        'author': 'question_author',
        'author_initials': 'QA',
        'created_at': '2 часа назад',
        'likes': 24,
    }
    answers = make_answers(7, question_id)
    page = paginate(answers, request, per_page=5)
    ctx = base_context()
    ctx.update({'question': q, 'page_obj': page})
    return render(request, 'questions/question.html', ctx)


def ask(request):
    ctx = base_context()
    return render(request, 'questions/ask.html', ctx)
