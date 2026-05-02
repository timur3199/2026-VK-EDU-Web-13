from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from questions.models import Profile

ALLOWED_AVATAR_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
MAX_AVATAR_SIZE = 2 * 1024 * 1024  # 2 MB


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        password = cleaned.get('password')
        if username and password:
            self._user = authenticate(username=username, password=password)
            if self._user is None:
                raise forms.ValidationError('Неверный логин или пароль.')
            if not self._user.is_active:
                raise forms.ValidationError('Аккаунт отключён.')
        return cleaned

    
    
    def get_user(self):
        return self._user


class SignupForm(forms.ModelForm):
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email
    
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Не менее 8 символов'}),
    )
    password_confirm = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')
        labels = {'username': 'Логин', 'email': 'Email', 'first_name': 'Имя'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте логин'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('password_confirm')
        if password and confirm and password != confirm:
            self.add_error('password_confirm', 'Пароли не совпадают.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        label='Аватар',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')
        labels = {'username': 'Логин', 'email': 'Email', 'first_name': 'Имя'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот логин уже занят.')
        return username

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:
            return avatar
        import os
        ext = os.path.splitext(avatar.name)[1].lower()
        if ext not in ALLOWED_AVATAR_EXTENSIONS:
            raise forms.ValidationError(
                f'Недопустимый формат. Разрешены: {", ".join(ALLOWED_AVATAR_EXTENSIONS)}'
            )
        if avatar.size > MAX_AVATAR_SIZE:
            raise forms.ValidationError('Файл слишком большой. Максимум 2 МБ.')
        return avatar

    def save(self, commit=True):
        user = super().save(commit=True)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.avatar = avatar
            profile.save()
        return user
    
    
