from django.contrib import admin
from .models import QuizTopic, Question, Answer

@admin.register(QuizTopic)
class QuizTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'created_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
