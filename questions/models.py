from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class QuizTopic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    topic = models.ForeignKey(QuizTopic, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)
    allow_multiple = models.BooleanField(default=False)  # New field
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} (Correct: {self.is_correct})"
