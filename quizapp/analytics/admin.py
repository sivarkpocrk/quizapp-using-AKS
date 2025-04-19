from django.contrib import admin
from .models import UserQuizAttempt, UserAnswer

@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'score', 'date_taken')
    list_filter = ('topic', 'date_taken')
    search_fields = ('user__username', 'topic__name')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'answer', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('question__text', 'answer__text')
