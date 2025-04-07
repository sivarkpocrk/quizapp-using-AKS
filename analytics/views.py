from django.shortcuts import render
from .models import UserQuizAttempt, UserAnswer

def user_analytics(request):
    attempts = UserQuizAttempt.objects.all()
    return render(request, 'analytics/analytics.html', {'attempts': attempts})
