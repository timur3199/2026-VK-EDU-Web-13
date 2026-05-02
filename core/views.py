from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import LoginForm, SignupForm, ProfileForm


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('index')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = reverse('index')

    if request.user.is_authenticated:
        return redirect(next_url)

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(next_url)

    return render(request, 'core/login.html', {'form': form, 'next': next_url})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('index')

    return render(request, 'core/signup.html', {'form': form})


@login_required(login_url='/login/')
def profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'core/profile.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('index')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = reverse('index')
    return redirect(next_url)
