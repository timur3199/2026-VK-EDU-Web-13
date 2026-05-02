from django import forms
from .models import Question, Answer, Tag


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        label='Теги',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'python, django, api  (через запятую, до 5 тегов)',
        }),
        help_text='До 5 тегов через запятую.',
    )

    class Meta:
        model = Question
        fields = ('title', 'text')
        labels = {'title': 'Заголовок', 'text': 'Описание'}
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кратко опишите суть вопроса…',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Подробно опишите вашу проблему…',
            }),
        }

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        names = [t.strip().lower() for t in raw.split(',') if t.strip()]
        if len(names) > 5:
            raise forms.ValidationError('Не более 5 тегов.')
        return names

    def save(self, author, commit=True):
        question = super().save(commit=False)
        question.author = author
        if commit:
            question.save()
            tag_names = self.cleaned_data.get('tags', [])
            tag_objs = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tag_objs.append(tag)
            question.tags.set(tag_objs)
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        labels = {'text': 'Ваш ответ'}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Напишите ваш ответ…',
            }),
        }

    def save(self, author, question, commit=True):
        answer = super().save(commit=False)
        answer.author = author
        answer.question = question
        if commit:
            answer.save()
            question.answers_count = question.answers.count()
            question.save(update_fields=['answers_count'])
        return answer
