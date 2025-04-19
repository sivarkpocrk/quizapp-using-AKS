from django.shortcuts import render
from questions.models import QuizTopic  # Import from questions app

def home(request):
    quiz_topics = QuizTopic.objects.all()
    return render(request, 'main/home.html', {'quiz_topics': quiz_topics})
