from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserQuizAttempt


@login_required
def analytics_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        attempts = UserQuizAttempt.objects.all().order_by('-date_taken')
    else:
        attempts = UserQuizAttempt.objects.filter(user=request.user).order_by('-date_taken')

    return render(request, 'analytics/dashboard.html', {'attempts': attempts})
