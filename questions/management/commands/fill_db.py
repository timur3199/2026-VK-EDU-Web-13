import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from questions.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

fake_ru = Faker('ru_RU')
fake_en = Faker('en_US')

TECH_TAGS = [
    'python', 'django', 'javascript', 'react', 'vue', 'typescript',
    'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes',
    'git', 'linux', 'nginx', 'api', 'rest', 'graphql', 'sql', 'css',
    'html', 'node', 'fastapi', 'flask', 'celery', 'async', 'orm', 'jwt',
    'testing', 'ci', 'devops', 'aws', 'security', 'performance', 'websocket',
    'microservices', 'architecture', 'algorithms', 'data-structures', 'regex',
    'json', 'xml', 'http', 'oauth', 'cors', 'crud', 'mvc', 'solid',
]


class Command(BaseCommand):
    help = 'Заполнить базу данных. Пример: python manage.py fill_db 100'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, nargs='?', default=1)

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(f'Заполнение БД с ratio={ratio}...')

        users = self.fill_users(ratio)
        tags = self.fill_tags(ratio)
        questions = self.fill_questions(ratio, users, tags)
        answers = self.fill_answers(ratio, users, questions)
        self.fill_likes(ratio, users, questions, answers)

        self.stdout.write(self.style.SUCCESS(
            f'Готово! {len(users)} пользователей, {len(questions)} вопросов, '
            f'{len(answers)} ответов, {len(tags)} тегов'
        ))

    def fill_users(self, ratio):
        self.stdout.write('Создание пользователей...')
        users_to_create = [
            User(
                username=(fake_en.user_name() + str(random.randint(100, 9999)))[:150],
                email=fake_en.email(),
                first_name=fake_ru.first_name(),
                last_name=fake_ru.last_name(),
            )
            for _ in range(ratio)
        ]
        User.objects.bulk_create(users_to_create, ignore_conflicts=True)
        users = list(User.objects.order_by('-id')[:ratio])
        existing_ids = set(Profile.objects.values_list('user_id', flat=True))
        Profile.objects.bulk_create(
            [Profile(user=u) for u in users if u.id not in existing_ids],
            ignore_conflicts=True
        )
        return users

    def fill_tags(self, ratio):
        self.stdout.write('Создание тегов...')
        tag_names = TECH_TAGS[:min(ratio, len(TECH_TAGS))]
        Tag.objects.bulk_create(
            [Tag(name=name) for name in tag_names], ignore_conflicts=True
        )
        return list(Tag.objects.all())

    def fill_questions(self, ratio, users, tags):
        self.stdout.write('Создание вопросов...')
        questions_to_create = [
            Question(
                author=random.choice(users),
                title=fake_ru.sentence(nb_words=8)[:255],
                text=fake_ru.paragraph(nb_sentences=5),
                likes_count=random.randint(0, 100),
                answers_count=0,
            )
            for _ in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions_to_create)
        questions = list(Question.objects.order_by('-id')[:ratio * 10])
        self.stdout.write('Добавление тегов к вопросам...')
        for question in questions:
            question.tags.set(random.sample(tags, min(3, len(tags))))
        return questions

    def fill_answers(self, ratio, users, questions):
        self.stdout.write('Создание ответов...')
        Answer.objects.bulk_create([
            Answer(
                question=random.choice(questions),
                author=random.choice(users),
                text=fake_ru.paragraph(nb_sentences=3),
                is_correct=random.random() < 0.1,
                likes_count=random.randint(0, 50),
            )
            for _ in range(ratio * 100)
        ])
        answers = list(Answer.objects.order_by('-id')[:ratio * 100])
        for q in questions:
            q.answers_count = q.answers.count()
        Question.objects.bulk_update(questions, ['answers_count'])
        return answers

    def fill_likes(self, ratio, users, questions, answers):
        self.stdout.write('Создание лайков...')
        target = ratio * 100

        q_likes, seen_q = [], set()
        for _ in range(target * 3):
            if len(q_likes) >= target:
                break
            key = (random.choice(users).id, random.choice(questions).id)
            if key not in seen_q:
                seen_q.add(key)
                q_likes.append(QuestionLike(user_id=key[0], question_id=key[1]))
        QuestionLike.objects.bulk_create(q_likes, ignore_conflicts=True)

        a_likes, seen_a = [], set()
        for _ in range(target * 3):
            if len(a_likes) >= target:
                break
            key = (random.choice(users).id, random.choice(answers).id)
            if key not in seen_a:
                seen_a.add(key)
                a_likes.append(AnswerLike(user_id=key[0], answer_id=key[1]))
        AnswerLike.objects.bulk_create(a_likes, ignore_conflicts=True)
