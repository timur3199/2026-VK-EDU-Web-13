from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Question, Tag, Profile
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
    tag_obj = get_object_or_404(Tag, name=tag_name)
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
            # Redirect to the page containing the new answer
            answers_list = list(q.answers.order_by('-is_correct', '-likes_count').values_list('id', flat=True))
            answer_index = list(answers_list).index(answer.id) + 1
            page_num = (answer_index - 1) // 5 + 1
            return redirect(f'/question/{question_id}/?page={page_num}#answer-{answer.id}')

    page_obj = paginate(answers, request, 5)
    ctx = base_context()
    ctx.update({'question': q, 'page_obj': page_obj, 'answer_form': form})
    return render(request, 'questions/question.html', ctx)


@login_required(login_url='/login/')
def ask(request):
    form = QuestionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        q = form.save(author=request.user)
        return redirect('question', question_id=q.pk)
    return render(request, 'questions/ask.html', {**base_context(), 'form': form})
