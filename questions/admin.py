from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike


# ─── Inlines ──────────────────────────────────────────────────────────────────

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    raw_id_fields = ('author',)
    fields = ('author', 'text', 'is_correct', 'likes_count')
    readonly_fields = ('likes_count',)


# ─── Extended UserAdmin ────────────────────────────────────────────────────────

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ─── Model Admins ─────────────────────────────────────────────────────────────

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'likes_count', 'answers_count', 'created_at')
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('created_at', 'tags')
    raw_id_fields = ('author',)
    filter_horizontal = ('tags',)
    inlines = (AnswerInline,)
    readonly_fields = ('likes_count', 'answers_count', 'created_at')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'is_correct', 'likes_count', 'created_at')
    search_fields = ('text', 'author__username', 'question__title')
    list_filter = ('is_correct', 'created_at')
    raw_id_fields = ('author', 'question')
    readonly_fields = ('likes_count', 'created_at')


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question')
    search_fields = ('user__username', 'question__title')
    raw_id_fields = ('user', 'question')


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer')
    search_fields = ('user__username',)
    raw_id_fields = ('user', 'answer')
