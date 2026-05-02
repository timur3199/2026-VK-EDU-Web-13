from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Question, Answer, Tag, Profile, QuestionLike, AnswerLike
from .forms import QuestionForm, AnswerForm


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


def base_context():
    return {
        'popular_tags': Tag.objects.order_by('name')[:15],
        'top_members': Profile.objects.select_related('user').order_by('-id')[:5],
    }


def index(request):
    ctx = base_context()
    ctx['page_obj'] = paginate(Question.objects.new(), request, 5)
    ctx['active_tab'] = 'new'
    return render(request, 'questions/index.html', ctx)


def hot(request):
    ctx = base_context()
    ctx['page_obj'] = paginate(Question.objects.hot(), request, 5)
    ctx['active_tab'] = 'hot'
    return render(request, 'questions/hot.html', ctx)


def tag(request, tag_name):
    get_object_or_404(Tag, name=tag_name)
    ctx = base_context()
    ctx['page_obj'] = paginate(Question.objects.by_tag(tag_name), request, 5)
    ctx['tag_name'] = tag_name
    return render(request, 'questions/tag.html', ctx)


def question(request, question_id):
    q = get_object_or_404(
        Question.objects.select_related('author__profile').prefetch_related('tags'),
        pk=question_id,
    )
    answers = q.answers.select_related('author__profile').order_by('-is_correct', '-likes_count')
    form = AnswerForm(request.POST or None)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/login/?next=/question/{question_id}/')
        if form.is_valid():
            answer = form.save(author=request.user, question=q)
            answers_ids = list(
                q.answers.order_by('-is_correct', '-likes_count').values_list('id', flat=True)
            )
            answer_index = answers_ids.index(answer.id) + 1
            page_num = (answer_index - 1) // 5 + 1
            return redirect(f'/question/{question_id}/?page={page_num}#answer-{answer.id}')

    # Collect liked IDs for current user
    liked_question_ids = set()
    liked_answer_ids = set()
    if request.user.is_authenticated:
        liked_question_ids = set(
            QuestionLike.objects.filter(user=request.user, question=q).values_list('question_id', flat=True)
        )
        liked_answer_ids = set(
            AnswerLike.objects.filter(
                user=request.user,
                answer__in=answers
            ).values_list('answer_id', flat=True)
        )

    page_obj = paginate(answers, request, 5)
    ctx = base_context()
    ctx.update({
        'question': q,
        'page_obj': page_obj,
        'answer_form': form,
        'liked_question_ids': liked_question_ids,
        'liked_answer_ids': liked_answer_ids,
    })
    return render(request, 'questions/question.html', ctx)


@login_required(login_url='/login/')
def ask(request):
    form = QuestionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        q = form.save(author=request.user)
        return redirect('question', question_id=q.pk)
    return render(request, 'questions/ask.html', {**base_context(), 'form': form})


# ─── AJAX views ───────────────────────────────────────────────────────────────

@require_POST
@login_required(login_url='/login/')
def question_like(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        QuestionLike.objects.create(user=request.user, question=q)
        q.likes_count += 1
        q.save(update_fields=['likes_count'])
        liked = True
    except IntegrityError:
        # Already liked — remove like
        QuestionLike.objects.filter(user=request.user, question=q).delete()
        q.likes_count = max(0, q.likes_count - 1)
        q.save(update_fields=['likes_count'])
        liked = False
    return JsonResponse({'likes_count': q.likes_count, 'liked': liked})


@require_POST
@login_required(login_url='/login/')
def answer_like(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    try:
        AnswerLike.objects.create(user=request.user, answer=answer)
        answer.likes_count += 1
        answer.save(update_fields=['likes_count'])
        liked = True
    except IntegrityError:
        AnswerLike.objects.filter(user=request.user, answer=answer).delete()
        answer.likes_count = max(0, answer.likes_count - 1)
        answer.save(update_fields=['likes_count'])
        liked = False
    return JsonResponse({'likes_count': answer.likes_count, 'liked': liked})


@require_POST
@login_required(login_url='/login/')
def mark_correct(request, answer_id):
    answer = get_object_or_404(Answer.objects.select_related('question__author'), pk=answer_id)
    if answer.question.author != request.user:
        return JsonResponse({'error': 'Только автор вопроса может отмечать правильный ответ.'}, status=403)
    # Toggle: unmark previous correct answer, mark this one
    was_correct = answer.is_correct
    Answer.objects.filter(question=answer.question, is_correct=True).update(is_correct=False)
    if not was_correct:
        answer.is_correct = True
        answer.save(update_fields=['is_correct'])
    return JsonResponse({'is_correct': answer.is_correct, 'answer_id': answer.id})
