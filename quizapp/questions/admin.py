from django.contrib import admin
from .models import QuizTopic, Question, Answer, Comment

@admin.register(QuizTopic)
class QuizTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'question_number', 'text', 'topic',
        'allow_multiple', 'has_correct_answer', 'correct_answer_count', 'created_at'
    )
    list_filter = ('topic', 'allow_multiple', 'has_correct_answer', 'created_at')  # ✅ Sidebar filters
    search_fields = ('question_number', 'text', 'topic__name')  # 🔍 Search bar
    ordering = ('question_number',)  # 📊 Order by question number


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_correct', 'question')
    list_filter = ('is_correct', 'question__topic')           # ✅ Filters
    search_fields = ('text', 'question__text')                # 🔍 Search answers
    ordering = ('question',)                                  # Sort answers by question

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text')
    search_fields = ('text', 'question__text')
    ordering = ('question',)
