from django.contrib import admin
from .models import UserQuizAttempt, UserAnswer

@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'score', 'date_taken')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'answer', 'is_correct')
