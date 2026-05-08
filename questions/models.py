from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# ─── Managers ─────────────────────────────────────────────────────────────────

class QuestionManager(models.Manager):
    def new(self):
        return self.select_related('author__profile').prefetch_related('tags').order_by('-created_at')

    def hot(self):
        return self.select_related('author__profile').prefetch_related('tags').order_by('-likes_count')

    def by_tag(self, tag_name):
        return self.select_related('author__profile').prefetch_related('tags').filter(tags__name=tag_name).order_by('-created_at')


# ─── Models ───────────────────────────────────────────────────────────────────

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,
                               verbose_name='Аватар')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'

    def get_initials(self):
        name = self.user.get_full_name()
        if name:
            parts = name.split()
            return (parts[0][0] + parts[1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()
        return self.user.username[:2].upper()


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions',
                               verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions',
                                  verbose_name='Теги')
    likes_count = models.IntegerField(default=0, verbose_name='Лайки')
    answers_count = models.IntegerField(default=0, verbose_name='Ответов')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.pk})


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers',
                                 verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers',
                               verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    likes_count = models.IntegerField(default=0, verbose_name='Лайки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'Ответ на «{self.question.title}» от {self.author.username}'


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes',
                             verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes',
                                 verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'
        unique_together = ('user', 'question')

    def __str__(self):
        return f'{self.user.username} → {self.question.title}'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes',
                             verbose_name='Пользователь')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes',
                               verbose_name='Ответ')

    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
        unique_together = ('user', 'answer')

    def __str__(self):
        return f'{self.user.username} → ответ #{self.answer.id}'
