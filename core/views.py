from django.shortcuts import render


TAGS = ['python', 'javascript', 'django', 'react', 'postgresql',
        'docker', 'api', 'sql', 'css', 'linux']

MEMBERS = [
    {'initials': 'АП', 'name': 'aleksey_p', 'score': 842},
    {'initials': 'МК', 'name': 'maria_k',   'score': 719},
    {'initials': 'ИС', 'name': 'ivan_s',    'score': 634},
    {'initials': 'ДВ', 'name': 'dmitry_v',  'score': 571},
    {'initials': 'НО', 'name': 'natasha_o', 'score': 498},
]


def base_context():
    return {'tags': TAGS, 'members': MEMBERS}


def login(request):
    return render(request, 'core/login.html', base_context())


def signup(request):
    return render(request, 'core/signup.html', base_context())


def profile(request):
    return render(request, 'core/profile.html', base_context())
