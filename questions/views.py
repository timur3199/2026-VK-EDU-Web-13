from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Question, Tag, Profile


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
    tags = Tag.objects.order_by('name')[:10]
    top_users = Profile.objects.select_related('user').order_by('-user__questions__likes_count')[:5]
    return {'popular_tags': tags, 'top_members': top_users}


def index(request):
    questions = Question.objects.new()
    ctx = base_context()
    ctx.update({'page_obj': paginate(questions, request, 5), 'active_tab': 'new'})
    return render(request, 'questions/index.html', ctx)


def hot(request):
    questions = Question.objects.hot()
    ctx = base_context()
    ctx.update({'page_obj': paginate(questions, request, 5), 'active_tab': 'hot'})
    return render(request, 'questions/hot.html', ctx)


def tag(request, tag_name):
    tag_obj = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.by_tag(tag_name)
    ctx = base_context()
    ctx.update({'page_obj': paginate(questions, request, 5), 'tag_name': tag_name})
    return render(request, 'questions/tag.html', ctx)


def question(request, question_id):
    q = get_object_or_404(Question.objects.select_related('author__profile').prefetch_related('tags'), pk=question_id)
    answers = q.answers.select_related('author__profile').order_by('-is_correct', '-likes_count')
    ctx = base_context()
    ctx.update({'question': q, 'page_obj': paginate(answers, request, 5)})
    return render(request, 'questions/question.html', ctx)


def ask(request):
    return render(request, 'questions/ask.html', base_context())
